"""Fig. 3.2.7 — bruit en boucle fermée, sortie V2 (gain de sortie 100) (p. 153)."""
from style import *

c = lire_courbes("bruit-fig-3-2-7")
st = {"Bruit 1/f en boucle ouverte (rappel)": dict(color=GRIS, ls="--", lw=0.9),
      "Étage de tête en boucle ouverte (rappel)": dict(color=GRIS, ls="--", lw=0.9),
      "Bruit de l'amplificateur de sortie": dict(color=VIOLET),
      "Bruit excédentaire": dict(color=ORANGE),
      "Bruit de l'étage de tête": dict(color=BLEU),
      "Majoration du bruit thermique de sortie": dict(color=GRIS, ls="--", lw=1.4)}
fig, ax = figure(6.3, 4.0)
for nom, d in c.items():
    ax.plot(d[:, 0], d[:, 1], label=nom, **st[nom])
ax.axvline(12, color=ENCRE2, lw=0.6); ax.axvline(1, color=ENCRE2, lw=0.6)
etiquette(ax, 12, -119, " $T_m$ = 12 s", fontsize=7); etiquette(ax, 1, -119, " $T_0$", fontsize=7)
ax.set_xscale("log"); axe_log(ax); ax.set_xlim(600, 0.07)
ax.set_xticks([400, 100, 10, 1, 0.1]); ax.set_xticklabels(["400 s", "100 s", "10 s", "1 s", "0,1 s"])
ax.set_xlabel("Période"); ax.set_ylim(-120, -38); ax.set_ylabel("dB réf. 1 V/$\\sqrt{\\mathrm{Hz}}$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=7)
sauver(fig, "fig-3-2-7")
