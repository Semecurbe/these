"""Numérisation des enregistrements papier (fig. 4.2.1, 4.2.5, 4.2.6) -> donnees/enregistrement-*.csv

Chaque voie est suivie colonne par colonne dans sa bande : quadrillage (lignes et colonnes
sombres sur une grande partie de la bande) retiré, puis choix du segment de tracé le plus
proche de la position précédente. Les ordonnées sont exprimées en unités de page (repère 827,
croissant vers le haut, origine au centre de la bande) ; la conversion en unités physiques
(échelles des légendes) est faite par les scripts de tracé.
"""
import sys
from pathlib import Path
import numpy as np
from outils import K, page, segments, ecrire_csv

DONNEES = Path(__file__).resolve().parents[1] / "donnees"

# nom : page, x0, x1, [bandes (y0, y1, départ)], seuils de quadrillage
CONFIG = {
    "enregistrement-4-2-1": dict(page=180, x=(68, 797), bandes=[(440, 480, 455, 6), (553, 632, 588, 6), (695, 742, 716, 6), (808, 905, 862, 6)],
                                 grille_v=0.25, grille_h=0.5, ligne_max=45, ecart=12.0),
    "enregistrement-4-2-5": dict(page=185, x=(22, 783), bandes=[(432, 535, 475), (550, 695, 640), (700, 788, 720)],
                                 grille_v=0.75, grille_h=0.5, ligne_max=180, coupes={2: (22, 755)}, masques={2: [(195, 550, 480, 697)]}),
    "enregistrement-4-2-6": dict(page=187, x=(27, 790), bandes=[(262, 330, 290), (482, 545, 505)],
                                 grille_v=0.75, grille_h=0.5, ligne_max=120, coupes={1: (80, 790)}, masques={1: [(225, 300, 250, 330)]}),
}


def suivre_bande(img, x0, x1, y0, y1, depart, gv, gh, saut=6.0, ligne_max=0, masques=()):
    """Chemin optimal (programmation dynamique) à travers les segments de tracé candidats de
    chaque colonne : minimise la somme des sauts verticaux ; les colonnes sans candidat sont
    ignorées. `depart` fixe le point de départ privilégié, `saut` borne les sauts (unités 827)."""
    X0, X1, Y0, Y1 = (int(round(v * K)) for v in (x0, x1, y0, y1))
    a = img[Y0:Y1, X0:X1] < 150
    col = a.mean(axis=0) > gv
    lig = a.mean(axis=1) > gh
    for v in (col, lig):
        for _ in range(2):
            v[1:] |= v[:-1].copy(); v[:-1] |= v[1:].copy()
    a[:, col] = False; a[lig, :] = False
    for mx0, my0, mx1, my1 in masques:
        a[max(int(my0 * K) - Y0, 0):max(int(my1 * K) - Y0, 0), max(int(mx0 * K) - X0, 0):max(int(mx1 * K) - X0, 0)] = False
    # traits horizontaux longs (bords de bande, pointillés de temps) : supprimés
    if ligne_max:
        for r in range(a.shape[0]):
            ligne = a[r]
            if ligne.sum() < ligne_max:
                continue
            idx = np.flatnonzero(np.diff(np.r_[0, ligne.astype(int), 0]))
            for d, f in zip(idx[::2], idx[1::2]):
                if f - d >= ligne_max:
                    ligne[d:f] = False
    cols, cands = [], []
    for j in range(a.shape[1]):
        segs = [(d, f) for d, f in segments(a[:, j]) if f - d >= 1]
        if segs:
            cols.append(j); cands.append(np.array([(d + f) / 2 for d, f in segs]))
    if not cols:
        return np.array([]), np.array([])
    lim = saut * K
    cout = [np.abs(cands[0] - (depart * K - Y0)) * 0.2]
    prec = [np.full(len(cands[0]), -1)]
    for k in range(1, len(cols)):
        dj = cols[k] - cols[k - 1]
        d = np.abs(cands[k][:, None] - cands[k - 1][None, :])
        pen = np.where(d > lim * max(1, dj / 4), 1e6, d)
        tot = pen + cout[-1][None, :]
        i = np.argmin(tot, axis=1)
        cout.append(tot[np.arange(len(i)), i]); prec.append(i)
    # remontée
    k = len(cols) - 1; i = int(np.argmin(cout[-1])); chemin = []
    while k >= 0:
        chemin.append((cols[k], cands[k][i])); i = prec[k][i]; k -= 1
    chemin = chemin[::-1]
    xs = np.array([(X0 + j) / K for j, _ in chemin]); ys = np.array([(Y0 + c) / K for _, c in chemin])
    return xs, ys


def numeriser(nom):
    c = CONFIG[nom]; img = page(c["page"])
    for k, b in enumerate(c["bandes"], start=1):
        y0, y1, dep = b[:3]; saut = b[3] if len(b) > 3 else 6.0
        xa, xb = c.get("coupes", {}).get(k, c["x"])
        x, y = suivre_bande(img, xa, xb, y0, y1, dep, c["grille_v"], c["grille_h"], saut, c.get("ligne_max", 0),
                            c.get("masques", {}).get(k, ()))
        if len(y) > 30:  # suppression des points isolés (écart à la médiane glissante)
            h = 30
            med = np.array([np.median(y[max(0, i - h):i + h + 1]) for i in range(len(y))])
            ok = np.abs(y - med) <= c.get("ecart", 3.0)
            x, y = x[ok], y[ok]
        ecrire_csv(DONNEES / f"{nom}-voie{k}.csv", ["x_page", "y_page"], [x, y])
        print(nom, k, len(x))


if __name__ == "__main__":
    for n in sys.argv[1:] or CONFIG:
        numeriser(n)
