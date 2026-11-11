"""Fig. 3.3.2 — nouvelle électronique : vérification de la constance du bruit dans la dynamique (p. 162)."""
from style import *

fig, ax = figure(6.3, 3.8)
spectre(ax, "spectre-3-3-2-haut", color=ORANGE, label="courbe R (maximum de dynamique, PROM + $\\pi/2$)")
spectre(ax, "spectre-3-3-2-bas", color=BLEU, label="courbes V, O, M (pratiquement confondues)")
axe_spectre(ax)
ax.legend(loc="lower left")
sauver(fig, "fig-3-3-2")
