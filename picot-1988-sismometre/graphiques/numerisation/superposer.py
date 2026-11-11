"""Contrôle : superpose les données numérisées (donnees/spectre-*.csv) au scan original."""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from outils import Axe, K, page
from numeriser_spectres import CONFIG, DONNEES

def superposer(nom, sortie):
    c = CONFIG[nom]; img = page(c["page"])
    ax = Axe(*c["x"], log=True); ay = Axe(*c["y"])
    x0, y0, x1, y1 = c["cadre"]
    fig, a = plt.subplots(figsize=(10, 10 * (y1 - y0) / (x1 - x0)))
    a.imshow(img[int(y0 * K):int(y1 * K), int(x0 * K):int(x1 * K)], cmap="gray", extent=(x0, x1, y1, y0), alpha=0.6)
    for suf, col in [("", "red"), ("-haut", "red"), ("-bas", "deepskyblue")]:
        f = DONNEES / f"{nom}{suf}.csv"
        if f.exists():
            d = np.genfromtxt(f, delimiter=",", names=True)
            a.plot(ax.pixel(d["x"]), ay.pixel(d["y"]), ".", ms=1.5, color=col)
    a.set_xlim(x0, x1); a.set_ylim(y1, y0); a.set_title(nom)
    fig.savefig(sortie, dpi=70, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for n in sys.argv[2:] or CONFIG:
        superposer(n, out / f"sup-{n}.png")
