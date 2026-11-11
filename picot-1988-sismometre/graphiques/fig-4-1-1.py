"""Fig. 4.1.1 — spectres de bruit instrumental électronique en densité spectrale d'accélération (p. 172)."""
from style import *

fig, ax = figure(6.3, 4.2)
bruits_reference(ax)
c = lire_courbes("bruit-fig-4-1-1")
st = {"Bruit blanc (gain de tête)": dict(color=BLEU, ls="-."),
      "1/f : LBH-A": dict(color=AQUA), "1/f : LPZ-A": dict(color=ORANGE),
      "Bruit blanc (non légendé sur l'original)": dict(color=GRIS, lw=0.8, ls="-."),
      "1/f : étage de sortie": dict(color=VIOLET, ls="-."),
      "1/f : LVDT LBH-A": dict(color=AQUA, lw=2), "1/f : LVDT LPZ-A": dict(color=ORANGE, lw=2, ls="--")}
for nom, d in c.items():
    lab = None if "non légendé" in nom else nom
    ax.plot(d[:, 0], d[:, 1], label=lab, **st[nom])
axe_periodes(ax); ax.set_ylim(-222, -100)
ax.set_ylabel("dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4, fontsize=7)
sauver(fig, "fig-4-1-1")
