"""Fig. 2.3.12 — spectres de bruit sismique de référence (relevés sur l'original, p. 116)."""
from style import *

fig, ax = figure(6.3, 3.8)
bruits_reference(ax)
d = np.genfromtxt(DONNEES / "bruit-iris-M.csv", delimiter=",", names=True)
axe_periodes(ax); ax.set_ylim(-220, -100)
ax.set_ylabel("dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$")
ax.legend(loc="upper right", ncol=2)
sauver(fig, "fig-2-3-12")
