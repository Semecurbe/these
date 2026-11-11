"""Fig. 2.1.6 — déformée statique de la lame : comparaison expérience / calcul numérique (p. 48)."""
from style import *

fig, ax = figure(6.0, 3.0)
for nom, c, ls, lab in [("numerique", ORANGE, "--", "numérique"), ("experience", BLEU, "-", "expérience")]:
    d = lire_csv(f"deformee-lame-{nom}"); o = np.argsort(d["x_mm"])
    ax.plot(d["x_mm"][o], d["y_mm"][o], color=c, ls=ls, label=lab)
ax.set_xlim(-140, 5); ax.set_ylim(-10, 62); ax.set_aspect("equal")
ax.set_xlabel("$\\bar X$ (mm)"); ax.set_ylabel("$\\bar Y$ (mm)"); ax.legend(loc="lower center")
sauver(fig, "fig-2-1-6")
