"""Outils de numérisation des courbes de la thèse scannée.

Les pages sont rendues depuis le PDF original (300 dpi, mis en cache), puis :
- calibration des axes à partir de deux points de référence par axe (lin. ou log.) ;
- extraction automatique des tracés (pixels sombres, quadrillage et textes masqués),
  colonne par colonne, avec suivi de plusieurs courbes ;
- superposition d'une grille en unités physiques pour les relevés manuels.

Les coordonnées « scan » sont exprimées dans le repère d'une page de 827 px de large
(comme les recadrages), converties en interne à 300 dpi (facteur 2480/827).
"""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RACINE = Path(__file__).resolve().parents[2]
PDF = RACINE.parent / "Jean-Daniel Picot - 1988 - Etude d'un sismomètre.pdf"
CACHE = Path(__file__).resolve().parent / "_cache"
K = 2480 / 827


def page(n, rotation=0):
    """Image en niveaux de gris (np.uint8) de la page n du PDF original, à 300 dpi."""
    CACHE.mkdir(exist_ok=True)
    png = CACHE / f"p-{n:03d}.png"
    if not png.exists():
        subprocess.run(["pdftoppm", "-r", "300", "-gray", "-png", "-singlefile",
                        "-f", str(n), "-l", str(n), str(PDF), str(png.with_suffix(""))], check=True)
    im = Image.open(png).convert("L")
    if rotation:
        im = im.rotate(rotation, expand=True)
    return np.asarray(im)


class Axe:
    """Correspondance pixel (repère 827) <-> valeur, linéaire ou logarithmique."""

    def __init__(self, p1, v1, p2, v2, log=False):
        self.log = log
        f = np.log10 if log else (lambda v: v)
        self.a = (f(v2) - f(v1)) / (p2 - p1)
        self.b = f(v1) - self.a * p1

    def valeur(self, p):
        v = self.a * np.asarray(p, float) + self.b
        return 10 ** v if self.log else v

    def pixel(self, v):
        f = np.log10 if self.log else (lambda x: x)
        return (f(np.asarray(v, float)) - self.b) / self.a


GRILLE = {}  # quadrillage connu : {"x": [valeurs], "y": [valeurs], "ax": Axe, "ay": Axe}


def masque_trace(img, cadre, masques=(), seuil=140, grille=0.55, grille_v=0.22, epaisseur=3):
    """Pixels de tracé dans le cadre (x0, y0, x1, y1 en repère 827) : sombres, hors quadrillage
    (lignes sombres sur plus de `grille` de la largeur, colonnes sur plus de `grille_v` de la
    hauteur, élargies de `epaisseur` px) et hors rectangles `masques`."""
    x0, y0, x1, y1 = [int(round(v * K)) for v in cadre]
    a = img[y0:y1, x0:x1] < seuil
    lignes = a.mean(axis=1) > grille
    colonnes = a.mean(axis=0) > grille_v
    for v in (lignes, colonnes):
        for _ in range(epaisseur):
            v[1:] |= v[:-1].copy(); v[:-1] |= v[1:].copy()
    a[lignes, :] = False
    a[:, colonnes] = False
    # quadrillage calculé à partir de la calibration (plus sûr que la détection)
    # (chaque position calculée est recalée sur la ligne sombre la plus proche, à ±12 px)
    if GRILLE:
        brut = img[y0:y1, x0:x1] < seuil
        prof_l, prof_c = brut.mean(axis=1), brut.mean(axis=0)
        for v in GRILLE.get("y", []):
            p = int(round(GRILLE["ay"].pixel(v) * K)) - y0
            lo, hi = max(p - 12, 0), min(p + 13, len(prof_l))
            if lo >= hi:
                continue
            q = lo + int(np.argmax(prof_l[lo:hi]))
            a[max(q - 4, 0):q + 5, :] = False
        for v in GRILLE.get("x", []):
            p = int(round(GRILLE["ax"].pixel(v) * K)) - x0
            lo, hi = max(p - 12, 0), min(p + 13, len(prof_c))
            if lo >= hi:
                continue
            q = lo + int(np.argmax(prof_c[lo:hi]))
            a[:, max(q - 4, 0):q + 5] = False
    for m in masques:
        mx0, my0, mx1, my1 = [int(round(v * K)) for v in m]
        a[max(my0 - y0, 0):max(my1 - y0, 0), max(mx0 - x0, 0):max(mx1 - x0, 0)] = False
    return a, x0, y0


def segments(colonne):
    """Segments contigus de pixels vrais d'une colonne : liste (début, fin)."""
    idx = np.flatnonzero(colonne)
    if not len(idx):
        return []
    coupures = np.flatnonzero(np.diff(idx) > 2)
    debuts = np.r_[idx[0], idx[coupures + 1]]
    fins = np.r_[idx[coupures], idx[-1]]
    return list(zip(debuts, fins))


def filtre_median(y, largeur=15, ecart=None):
    """Médiane glissante ; si `ecart` est donné, renvoie aussi le masque des points proches."""
    n = len(y); h = largeur // 2
    m = np.array([np.median(y[max(0, i - h):i + h + 1]) for i in range(n)])
    return m if ecart is None else (m, np.abs(y - m) <= ecart)


def bords(img, cadre, ax, ay, masques=(), seuil=140, grille=0.55, min_seg=3):
    """Deux courbes d'un même graphique : bord supérieur du tracé le plus haut et bord inférieur
    du tracé le plus bas, colonne par colonne (segments plus fins que `min_seg` px ignorés :
    pointillés, asymptotes)."""
    a, x0, y0 = masque_trace(img, cadre, masques, seuil, grille)
    out = []
    for j in range(a.shape[1]):
        segs = [(d, f) for d, f in segments(a[:, j]) if f - d + 1 >= min_seg]
        if not segs:
            continue
        out.append((ax.valeur((x0 + j) / K), ay.valeur((y0 + segs[0][0]) / K), ay.valeur((y0 + segs[-1][1]) / K)))
    return np.array(out)


def enveloppe(img, cadre, ax, ay, masques=(), seuil=140, pas=1, grille=0.55):
    """Une seule courbe (éventuellement bruitée) : min/max/médiane par colonne -> x, ymin, ymax, ymed."""
    a, x0, y0 = masque_trace(img, cadre, masques, seuil, grille)
    out = []
    for j in range(0, a.shape[1], pas):
        idx = np.flatnonzero(a[:, j])
        if len(idx) == 0:
            continue
        px = (x0 + j) / K
        hi, lo, med = (y0 + idx.min()) / K, (y0 + idx.max()) / K, (y0 + np.median(idx)) / K
        out.append((ax.valeur(px), ay.valeur(lo), ay.valeur(hi), ay.valeur(med)))
    return np.array(out)


def suivre(img, cadre, ax, ay, departs, masques=(), seuil=140, saut=25, grille=0.55):
    """Suit plusieurs courbes de gauche à droite. `departs` : ordonnées (en valeurs) des courbes
    au bord gauche du cadre. Retourne une liste de tableaux (x, y) — un par courbe."""
    a, x0, y0 = masque_trace(img, cadre, masques, seuil, grille)
    pos = [float(ay.pixel(v) * K - y0) for v in departs]
    pistes = [[] for _ in departs]
    for j in range(a.shape[1]):
        segs = segments(a[:, j])
        if not segs:
            continue
        centres = np.array([(d + f) / 2 for d, f in segs])
        for k, p in enumerate(pos):
            i = np.argmin(np.abs(centres - p))
            if abs(centres[i] - p) <= saut * K / 3:
                pos[k] = 0.7 * centres[i] + 0.3 * p
                pistes[k].append((ax.valeur((x0 + j) / K), ay.valeur((y0 + centres[i]) / K)))
    return [np.array(p) for p in pistes]


def grille_donnees(img, cadre, ax, ay, xs, ys, sortie, zoom=1.0):
    """Superpose au scan une grille en unités physiques (pour relevés manuels) et l'enregistre."""
    x0, y0, x1, y1 = cadre
    im = Image.fromarray(img).convert("RGB")
    d = ImageDraw.Draw(im)
    for v in xs:
        p = ax.pixel(v) * K
        d.line([(p, y0 * K), (p, y1 * K)], fill=(255, 0, 0), width=1)
        d.text((p + 3, y1 * K + 4), f"{v:g}", fill=(255, 0, 0))
    for v in ys:
        p = ay.pixel(v) * K
        d.line([(x0 * K, p), (x1 * K, p)], fill=(0, 0, 255), width=1)
        d.text((x0 * K - 40, p - 6), f"{v:g}", fill=(0, 0, 255))
    c = im.crop((int(x0 * K) - 50, int(y0 * K) - 10, int(x1 * K) + 10, int(y1 * K) + 25))
    if zoom != 1:
        c = c.resize((int(c.width * zoom), int(c.height * zoom)), Image.LANCZOS)
    c.save(sortie)


def ecrire_csv(chemin, entetes, colonnes):
    np.savetxt(chemin, np.column_stack(colonnes), delimiter=",", header=",".join(entetes),
               comments="", fmt="%.6g")


def chemin(a, depart, biais=0.0, lim=40.0):
    """Chemin de coût minimal à travers les segments candidats de chaque colonne de `a` (masque
    booléen) : coût = somme des sauts verticaux (px) + `biais` × ordonnée (biais < 0 : préfère le
    haut, > 0 : le bas). Colonnes sans candidat ignorées. Renvoie (colonnes, lignes)."""
    cols, cands = [], []
    for j in range(a.shape[1]):
        segs = segments(a[:, j])
        if segs:
            cols.append(j); cands.append(np.array([(d + f) / 2 for d, f in segs], float))
    if not cols:
        return np.array([]), np.array([])
    cout = [np.abs(cands[0] - depart) + biais * cands[0]]
    prec = [np.full(len(cands[0]), -1)]
    for k in range(1, len(cols)):
        dj = cols[k] - cols[k - 1]
        d = np.abs(cands[k][:, None] - cands[k - 1][None, :])
        pen = np.where(d > lim * max(1.0, dj / 3), 1e6 + d, d)
        tot = pen + cout[-1][None, :]
        i = np.argmin(tot, axis=1)
        cout.append(tot[np.arange(len(i)), i] + biais * cands[k]); prec.append(i)
    k = len(cols) - 1; i = int(np.argmin(cout[-1])); res = []
    while k >= 0:
        res.append((cols[k], cands[k][i])); i = prec[k][i]; k -= 1
    res = res[::-1]
    return np.array([c for c, _ in res]), np.array([r for _, r in res])


def chemin_sauts(a, depart, biais=0.0, fenetre=40, penalite_saut=1.5, lim=30.0, recompense=2.5):
    """Comme `chemin`, mais le tracé peut sauter des colonnes (jusqu'à `fenetre`) : chaque colonne
    sautée coûte `penalite_saut` px. Les fragments parasites (quadrillage, textes) éloignés du
    tracé sont ainsi ignorés au lieu d'être imposés ; chaque point retenu rapporte `recompense`,
    et `biais` (sans dimension, ±1 à 2) favorise le haut (> 0) ou le bas (< 0) du cadre."""
    pts = []  # (colonne, ligne)
    for j in range(a.shape[1]):
        for d, f in segments(a[:, j]):
            pts.append((j, (d + f) / 2))
    if not pts:
        return np.array([]), np.array([])
    pts = np.array(pts)
    n = len(pts); cout = np.full(n, np.inf); prec = np.full(n, -1)
    col = pts[:, 0].astype(int); row = pts[:, 1]
    debut = col[0]
    # index des points par colonne
    from collections import defaultdict
    par_col = defaultdict(list)
    for i, c in enumerate(col):
        par_col[c].append(i)
    for i in range(n):
        c = col[i]
        best, bp = (c - debut) * penalite_saut + abs(row[i] - depart), -1  # départ direct
        for dc in range(1, fenetre + 1):
            for p in par_col.get(c - dc, ()):
                dr = abs(row[i] - row[p])
                if dr > lim * max(1.0, dc / 3):
                    continue
                v = cout[p] + dr + (dc - 1) * penalite_saut
                if v < best:
                    best, bp = v, p
        cout[i] = best - recompense + biais * row[i] / a.shape[0]; prec[i] = bp
    fin = col.max()
    i = int(np.argmin(cout + (fin - col) * penalite_saut))
    res = []
    while i >= 0:
        res.append(i); i = prec[i]
    res = res[::-1]
    return col[res], row[res]


def nettoyer(x, y, fenetre=61, ecart=2.5, palier=25):
    """Supprime les points aberrants (écart à la médiane glissante > `ecart`) et les paliers
    parfaitement plats de plus de `palier` points (fragments de quadrillage ou de texte)."""
    ok = np.ones(len(y), bool)
    i = 0
    while i < len(y):
        j = i
        while j + 1 < len(y) and y[j + 1] == y[i]:
            j += 1
        if j - i + 1 >= palier:
            ok[i:j + 1] = False
        i = j + 1
    x, y = x[ok], y[ok]
    med, ok2 = filtre_median(y, fenetre, ecart=ecart)
    return x[ok2], y[ok2]
