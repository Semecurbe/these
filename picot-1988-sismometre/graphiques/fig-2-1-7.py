"""Fig. 2.1.7 — premier mode parasite de la lame (73,66 Hz) : déformée statique et allure du mode
(mode relevé sur l'original p. 49, amplitude arbitraire)."""
from style import *

d = lire_csv("deformee-lame-experience"); o = np.argsort(d["x_mm"])
m = lire_csv("lame-mode1")
fig, ax = figure(6.0, 3.0)
ax.plot(d["x_mm"][o], d["y_mm"][o], color=BLEU, label="lame déformée (statique)")
xs = np.linspace(m["x_mm"].min(), m["x_mm"].max(), 300)
ys = np.interp(xs, m["x_mm"], m["y_mm"])
ys = np.convolve(np.pad(ys, 6, mode="edge"), np.ones(13) / 13, mode="valid")
ax.plot(xs, ys, color=ORANGE, ls="--", label="1$^{er}$ mode propre (73,66 Hz)")
for x, t in [(-132, "$K$"), (0, "$O$")]:
    ax.plot(x, 0 if x == 0 else 4, "s", ms=4, color=ENCRE2); etiquette(ax, x, -8, t, ha="center")
ax.set_xlim(-140, 6); ax.set_ylim(-12, 65); ax.set_aspect("equal")
ax.set_xlabel("$x$ (mm)"); ax.set_ylabel("$y$ (mm)"); ax.legend(loc="upper left", fontsize=7)
sauver(fig, "fig-2-1-7")
