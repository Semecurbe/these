"""Fig. 3.3.3 — analyse spectrale (voir la légende du document), courbe numérisée."""
from style import *

fig, ax = figure(6.3, 3.6)
spectre(ax, "spectre-3-3-3", color=BLEU)
axe_spectre(ax)
sauver(fig, "fig-3-3-3")
