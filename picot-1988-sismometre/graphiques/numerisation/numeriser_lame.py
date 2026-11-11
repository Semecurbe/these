"""Numérisation de la déformée de la lame (fig. 2.1.6, p. 53) -> donnees/deformee-lame-*.csv
Axes recalés sur les graduations (x : -140 -> 145,0 ; -40 -> 533,5 ; y : -10 sur l'axe à 608,9 ; même échelle)."""
from pathlib import Path
import numpy as np
from outils import Axe, page, bords, filtre_median, ecrire_csv

DONNEES = Path(__file__).resolve().parents[1] / "donnees"
img = page(53)
ax = Axe(145.0, -140, 533.5, -40)
ay = Axe(608.9, -10, 608.9 - 70 * (533.5 - 145.0) / 100, 60)
d = bords(img, (168, 345, 700, 600), ax, ay, masques=[(285, 515, 460, 575)], seuil=140, grille=0.9, min_seg=2)
for k, nom in [(1, "numerique"), (2, "experience")]:
    med, ok = filtre_median(d[:, k], 15, ecart=1.5)
    ecrire_csv(DONNEES / f"deformee-lame-{nom}.csv", ["x_mm", "y_mm"], [d[ok, 0], d[ok, k]])
    print(nom, ok.sum(), d[ok, 0].min(), d[ok, 0].max(), d[ok, k].max())
