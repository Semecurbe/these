"""Fig. 1.1 — performances de bruit recherchées (bruit sismique et bruit instrumental, p. 11)."""
from style import *

fig, ax = figure(6.3, 4.2)
bruits_reference(ax)
c = lire_courbes("instruments-fig-1-1")
st = {"ZM 500": dict(color=BLEU), "LPZ 12 s": dict(color=ORANGE), "LPH asservi": dict(color=AQUA)}
for nom, d in c.items():
    base = next(k for k in st if nom.startswith(k))
    ls = "-" if "électronique" in nom else (0, (1.5, 1.5))
    ax.plot(d[:, 0], d[:, 1], ls=ls, lw=1.3, label=nom, **st[base])
axe_periodes(ax); ax.set_ylim(-222, -100)
ax.set_ylabel("dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=7)
sauver(fig, "fig-1-1")
