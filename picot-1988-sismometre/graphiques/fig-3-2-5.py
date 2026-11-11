"""Fig. 3.2.5 — analyse théorique du bruit électronique en boucle ouverte, sortie V2 (p. 150).
Relevé des asymptotes tracées sur l'original."""
from style import *

c = lire_courbes("bruit-fig-3-2-5")
st = {"Bruit 1/f excédentaire (mesuré)": dict(color=ORANGE, ls="--", lw=1.6),
      "Bruit mesuré (blanc)": dict(color=ORANGE, ls="--", lw=1.6),
      "Bruit théorique étage de tête (G = 54.3 dB)": dict(color=BLEU),
      "Bruit théorique filtre 10.8 Hz": dict(color=AQUA),
      "Bruit théorique filtre 10.8 Hz (prolongement)": dict(color=AQUA, ls="--", lw=0.9),
      "Bruit théorique amplificateur de sortie (V2)": dict(color=VIOLET),
      "Majoration du bruit thermique de l'étage de sortie (V2)": dict(color=GRIS, ls="--")}
fig, ax = figure(6.3, 4.0)
for nom, d in c.items():
    lab = None if ("prolongement" in nom or nom == "Bruit mesuré (blanc)") else nom.replace("10.8", "10,8").replace("54.3", "54,3")
    ax.plot(d[:, 0], d[:, 1], label=lab, **st[nom])
ax.set_xscale("log"); axe_log(ax); ax.set_xlim(600, 0.07)
ax.set_xticks([400, 100, 10, 1, 0.1]); ax.set_xticklabels(["400 s", "100 s", "10 s", "1 s", "0,1 s"])
ax.set_xlabel("Période"); ax.set_ylim(-120, -38); ax.set_ylabel("dB réf. 1 V/$\\sqrt{\\mathrm{Hz}}$")
ax.legend(loc="lower left", fontsize=7)
etiquette(ax, 0.5, -62, "bruit mesuré", fontsize=7)
sauver(fig, "fig-3-2-5")
