"""Style commun des graphiques matplotlib de la thèse.

Chaque script graphiques/fig-*.py importe ce module, trace sa figure et appelle
sauver(fig, "fig-x-y-z") qui écrit figures/generees/<nom>.pdf (LaTeX) et .svg (HTML).

Palette : trois teintes catégorielles (palette de référence validée daltonisme),
plus un gris neutre pour les courbes de référence ; les styles de trait servent
d'encodage secondaire pour l'impression en noir et blanc.
"""
import subprocess
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "figures" / "generees"
DONNEES = Path(__file__).resolve().parent / "donnees"

# --- couleurs ---------------------------------------------------------------
BLEU, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
VIOLET = "#6250d6"
ENCRE, ENCRE2, GRIS, GRILLE = "#0b0b0b", "#52514e", "#8a8984", "#d9d8d4"
SERIES = [BLEU, ORANGE, AQUA]


def _police_latin_modern():
    """Enregistre Latin Modern (fournie par TinyTeX) pour l'accord avec les schémas TikZ."""
    noms = ["lmroman10-regular.otf", "lmroman10-italic.otf", "lmroman10-bold.otf"]
    trouvees = []
    for n in noms:
        try:
            p = subprocess.run(["kpsewhich", n], capture_output=True, text=True).stdout.strip()
        except FileNotFoundError:
            p = ""
        if not p:
            cand = Path.home() / ".TinyTeX/texmf-dist/fonts/opentype/public/lm" / n
            p = str(cand) if cand.exists() else ""
        if p:
            font_manager.fontManager.addfont(p)
            trouvees.append(p)
    return "Latin Modern Roman" if trouvees else "DejaVu Serif"


mpl.rcParams.update({
    "font.family": _police_latin_modern(),
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "axes.edgecolor": ENCRE2,
    "axes.labelcolor": ENCRE,
    "axes.linewidth": 0.6,
    "xtick.color": ENCRE2,
    "ytick.color": ENCRE2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.minor.width": 0.4,
    "ytick.minor.width": 0.4,
    "axes.grid": True,
    "axes.grid.which": "both",
    "grid.color": GRILLE,
    "grid.linewidth": 0.4,
    "lines.linewidth": 1.4,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
    "svg.fonttype": "path",
    "pdf.fonttype": 3,
    "axes.formatter.use_locale": False,
})


def figure(largeur=6.3, hauteur=3.6, **kw):
    """Crée une figure (dimensions en pouces ; 6,3 in ≈ largeur de texte A4)."""
    return plt.subplots(figsize=(largeur, hauteur), **kw)


def axe_log(ax, axe="x", decades=True):
    """Graduations logarithmiques avec grille mineure discrète."""
    a = ax.xaxis if axe == "x" else ax.yaxis
    a.set_major_locator(LogLocator(base=10, numticks=20))
    a.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=100))
    a.set_minor_formatter(NullFormatter())


def format_nombre(x, _pos=None):
    """Nombre à la française (virgule décimale, sans zéros inutiles)."""
    if x == 0:
        return "0"
    if abs(x) >= 1:
        s = f"{x:g}"
    else:
        s = f"{x:.10f}".rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def graduations_periodes(ax, valeurs=(0.01, 0.1, 1, 10, 100, 1000)):
    ax.xaxis.set_major_locator(FixedLocator(valeurs))
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))


def sauver(fig, nom):
    SORTIE.mkdir(parents=True, exist_ok=True)
    fig.savefig(SORTIE / f"{nom}.pdf")
    fig.savefig(SORTIE / f"{nom}.svg")
    plt.close(fig)


def lire_csv(nom):
    """Lit graphiques/donnees/<nom>.csv (en-tête sur la 1re ligne, séparateur virgule)."""
    return np.genfromtxt(DONNEES / f"{nom}.csv", delimiter=",", names=True)


def etiquette(ax, x, y, texte, **kw):
    """Étiquette directe en encre de texte (jamais dans la couleur de la série)."""
    kw.setdefault("fontsize", 8)
    kw.setdefault("color", ENCRE)
    return ax.text(x, y, texte, **kw)


# --- aides pour les spectres de bruit (axe des périodes, dB) -----------------
import csv as _csv


def lire_courbes(nom, cle="courbe"):
    """CSV long (courbe, x, y…) -> dict {courbe: tableau numpy des colonnes numériques}."""
    out = {}
    with open(DONNEES / f"{nom}.csv", encoding="utf-8") as f:
        r = _csv.DictReader(f)
        num = [c for c in r.fieldnames if c != cle and c != "type"]
        for ligne in r:
            out.setdefault(ligne[cle], []).append([float(ligne[c]) for c in num])
    return {k: np.array(v) for k, v in out.items()}


def axe_periodes(ax, tmin=0.01, tmax=1000, label="Période (s)"):
    ax.set_xscale("log"); axe_log(ax)
    ax.set_xlim(tmin, tmax)
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
    ax.set_xlabel(label)


def axe_frequences(ax, fmin, fmax, label="Fréquence (Hz)"):
    ax.set_xscale("log"); axe_log(ax)
    ax.set_xlim(fmin, fmax)
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
    ax.set_xlabel(label)


def bruits_reference(ax, labels=True, lajitas=True, qcaz=True):
    """Spectres de bruit sismique de référence (IRIS M et m, QCAZ, Lajitas) — fig. 2.3.12."""
    styles = [("iris-M", "IRIS M", dict(color=GRIS, lw=1.1)),
              ("iris-m", "IRIS m", dict(color=ENCRE2, lw=2.0))]
    if qcaz:
        styles.append(("qcaz", "QCAZ", dict(color=GRIS, lw=1.1, ls=(0, (6, 2, 1, 2)))))
    if lajitas:
        styles.append(("lajitas", "Lajitas", dict(color=GRIS, lw=1.1, ls=(0, (5, 2)))))
    for fichier, nom, st in styles:
        d = np.genfromtxt(DONNEES / f"bruit-{fichier}.csv", delimiter=",", names=True)
        ax.plot(d["periode_s"], d["db"], label=nom if labels else None, **st)


def texte(nom):
    """Convertit les exposants Unicode des noms de courbes (CSV) en mathtext."""
    for a, b in [("10⁵", "$10^5$"), ("10⁴", "$10^4$"), ("10⁶", "$10^6$"), ("s⁻¹", "s$^{-1}$"),
                 ("s⁻²", "s$^{-2}$"), ("mb =", "$m_b$ ="), ("Ms =", "$M_s$ =")]:
        nom = nom.replace(a, b)
    return nom


def spectre(ax, nom, **kw):
    """Trace un spectre numérisé (donnees/<nom>.csv, colonnes x, y)."""
    d = np.genfromtxt(DONNEES / f"{nom}.csv", delimiter=",", names=True)
    o = np.argsort(d["x"]); x, y = d["x"][o], d["y"][o]
    # les trous de la numérisation (textes masqués) restent des trous
    trou = np.flatnonzero(np.diff(np.log10(x)) > 0.03) + 1
    x = np.insert(x, trou, np.nan); y = np.insert(y, trou, np.nan)
    kw.setdefault("lw", 0.8)
    return ax.plot(x, y, **kw)


def axe_spectre(ax, fmin=0.0025, fmax=100, ymin=-90, ymax=-30):
    axe_frequences(ax, fmin, fmax)
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel("dB réf. 1 V$^2$/Hz")


NOTE_NUM = "courbe numérisée à partir de l'original"


def enregistrement(nom, voie):
    """Voie numérisée d'un enregistrement papier (unités de page, repère 827) -> (x, y) avec y
    croissant vers le haut et centré sur la moyenne, trous laissés vides."""
    d = np.genfromtxt(DONNEES / f"{nom}-voie{voie}.csv", delimiter=",", names=True)
    x, y = d["x_page"], -(d["y_page"] - np.mean(d["y_page"]))
    trou = np.flatnonzero(np.diff(x) > 3) + 1
    return np.insert(x, trou, np.nan), np.insert(y, trou, np.nan)
