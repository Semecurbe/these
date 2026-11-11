"""Fig. 3.3.4 — analyse spectrale (voir la légende du document), courbe numérisée."""
from style import *

fig, ax = figure(6.3, 3.6)
spectre(ax, "spectre-3-3-4", color=BLEU, label="primaire court-circuité à la masse et sur l'excitation (courbes confondues)")
ax.legend(loc="lower left")
axe_spectre(ax)
sauver(fig, "fig-3-3-4")
