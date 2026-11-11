"""Numérisation automatique des spectres mesurés (analyseur) -> graphiques/donnees/spectre-*.csv

Usage : python3 numeriser_spectres.py [--controle DOSSIER] [nom ...]
Avec --controle, une image de contrôle (tracé extrait superposé au scan) est écrite par figure.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import outils
from outils import Axe, K, page, enveloppe, bords, filtre_median, ecrire_csv, nettoyer

DONNEES = Path(__file__).resolve().parents[1] / "donnees"

# nom : page, cadre intérieur (repère 827), axe x (p1, v1, p2, v2), axe y (p1, v1, p2, v2),
#       mode ("enveloppe" | liste des départs pour le suivi), masques (textes)
CONFIG = {
    "spectre-3-2-6A": dict(page=158, cadre=(170, 130, 704, 522), x=(239.1, 0.01, 705.6, 100), y=(127.7, -30, 524.5, -90),
                           mode="une", plage_px=(172, 668), masques=[(500, 130, 704, 245), (172, 248, 232, 262), (525, 255, 575, 270), (450, 372, 505, 388), (640, 130, 704, 345)]),
    "spectre-3-2-6B": dict(page=158, cadre=(163, 570, 664, 928), x=(276.8, 0.01, 645.9, 1), y=(568.2, 0, 930.2, -60),
                           mode="une", masques=[(440, 569, 666, 680)]),
    "spectre-3-3-2": dict(page=168, cadre=(102, 158, 736, 628), x=(182.4, 0.01, 738.0, 100), y=(156.6, -30, 629.8, -90),
                          mode="deux", masques=[(176, 158, 206, 190), (180, 236, 214, 272), (136, 248, 170, 310), (488, 372, 538, 450), (586, 372, 612, 398), (105, 545, 165, 556)]),
    "spectre-3-3-3": dict(page=169, cadre=(58, 219, 682, 681), x=(137.2, 0.01, 683.5, 100), y=(217.7, -30, 682.6, -90),
                          mode="une", masques=[]),
    "spectre-3-3-4": dict(page=170, cadre=(73, 227, 696, 685), x=(153.2, 0.01, 697.6, 100), y=(225.8, -30, 686.8, -90),
                          mode="une", plage_px=(75, 650), masques=[]),
    "spectre-3-3-5": dict(page=171, cadre=(43, 105, 674, 576), x=(123.9, 0.01, 675.3, 100), y=(104.0, -30, 577.1, -90),
                          mode="une", masques=[]),
    "spectre-3-3-6a": dict(page=173, cadre=(85, 92, 641, 503), x=(155.6, 0.01, 642.4, 100), y=(90.7, -30, 504.4, -90),
                           mode="deux", seuil=115, fusion_px=400, masques=[(195, 155, 345, 166), (595, 431, 642, 443), (100, 152, 160, 166), (328, 316, 372, 336), (372, 370, 400, 392), (150, 175, 245, 225), (150, 300, 245, 350), (395, 160, 545, 225)]),
    "spectre-3-3-6b": dict(page=173, cadre=(85, 575, 643, 987), x=(156.2, 0.01, 644.3, 100), y=(573.4, -30, 988.4, -90),
                           mode="deux", seuil=115, fusion_px=400, masques=[(585, 702, 615, 714), (402, 888, 470, 920), (165, 735, 265, 790), (165, 855, 265, 905), (395, 640, 545, 705)]),
    "spectre-4-2-2": dict(page=181, cadre=(122, 121, 711, 539), x=(256.1, 0.01, 713.3, 1), y=(119.0, 20, 540.9, -60),
                          mode="deux", fusion_px=335, masques=[(120, 290, 330, 539), (118, 270, 258, 281), (148, 165, 205, 176), (160, 217, 190, 228), (695, 515, 712, 526), (178, 160, 215, 180), (470, 165, 711, 240), (355, 124, 485, 155), (180, 130, 250, 165), (128, 185, 190, 215)]),
    "spectre-4-2-3": dict(page=183, cadre=(118, 86, 697, 504), x=(250.3, 100, 698.8, 1), y=(189.7, -20, 399.5, -60),
                          mode="une", masques=[(118, 86, 697, 140), (118, 212, 260, 230)]),
}


def numeriser(nom, controle=None):
    c = CONFIG[nom]
    img = page(c["page"])
    ax = Axe(*c["x"], log=True); ay = Axe(*c["y"])
    pas = c.get("pas_y", 10)
    outils.GRILLE.clear()
    outils.GRILLE.update(ax=ax, ay=ay, y=list(range(-200, 60, pas)),
                         x=[m * 10.0 ** e for e in range(-4, 4) for m in range(1, 10)])
    if c["mode"] == "une":
        d = enveloppe(img, c["cadre"], ax, ay, c["masques"], seuil=c.get("seuil", 140))
        if "plage_px" in c:
            lo, hi = ax.valeur(np.array(c["plage_px"]))
            d = d[(d[:, 0] >= min(lo, hi)) & (d[:, 0] <= max(lo, hi))]
        med, ok = filtre_median(d[:, 3], 21, ecart=4.0)
        d = d[ok]
        ecrire_csv(DONNEES / f"{nom}.csv", ["x", "ymin", "ymax", "y"], [d[:, 0], d[:, 1], d[:, 2], d[:, 3]])
        traces = [d[:, [0, 3]]]
    else:
        d = bords(img, c["cadre"], ax, ay, c["masques"], seuil=c.get("seuil", 140))
        if "fusion_px" in c:  # au-delà, les deux courbes sont confondues sur l'original
            xf = ax.valeur(c["fusion_px"])
            apres = d[:, 0] > xf if ax.a > 0 else d[:, 0] < xf
            d[apres, 2] = d[apres, 1]
        traces = []
        for k in (1, 2):
            x, y = nettoyer(d[:, 0], d[:, k])
            traces.append(np.column_stack([x, y]))
        for i, t in enumerate(traces):
            ecrire_csv(DONNEES / f"{nom}-{'haut' if i == 0 else 'bas'}.csv", ["x", "y"], [t[:, 0], t[:, 1]])
    if controle:
        im = Image.fromarray(img).convert("RGB"); dr = ImageDraw.Draw(im)
        for t, col in zip(traces, [(255, 0, 0), (0, 120, 255)]):
            for x, y in t:
                px, py = ax.pixel(x) * K, ay.pixel(y) * K
                dr.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
        x0, y0, x1, y1 = c["cadre"]
        im.crop((int(x0 * K), int(y0 * K), int(x1 * K), int(y1 * K))).resize((int((x1 - x0) * 1.2), int((y1 - y0) * 1.2))).save(Path(controle) / f"{nom}.png")
    print(nom, [len(t) for t in traces])


if __name__ == "__main__":
    args = sys.argv[1:]; controle = None
    if "--controle" in args:
        i = args.index("--controle"); controle = args[i + 1]; del args[i:i + 2]
    for n in (args or CONFIG):
        numeriser(n, controle)
