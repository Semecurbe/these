"""Fig. 4.2.4 (bas) — courbe de réponse en accélération, sortie PCM gain 1000 (relevé, p. 177)."""
from style import *

c = lire_courbes("reponse-fig-4-2-4")
fig, ax = figure(5.6, 2.8)
ax.plot(c["réponse"][:, 0], c["réponse"][:, 1], color=BLEU, lw=1.6, label="réponse")
ax.plot(c["asymptotes"][:, 0], c["asymptotes"][:, 1], color=GRIS, lw=0.9, label="asymptotes")
axe_periodes(ax, 2, 3000); ax.invert_xaxis(); ax.set_ylim(60, 145)
ax.set_ylabel("dB réf. 1 V/(m s$^{-2}$)"); ax.legend(loc="lower left")
sauver(fig, "fig-4-2-4b")
