"""Fig. 4.2.2 — comparaison LPZ-12 s (vitesse) et LPZ-A : analyses spectrales à Lormes, 23/4/86 (p. 174)."""
from style import *

fig, ax = figure(6.3, 3.6)
spectre(ax, "spectre-4-2-2-haut", color=ORANGE, label="LPZ-12 s")
spectre(ax, "spectre-4-2-2-bas", color=BLEU, label="LPZ-A")
ax.annotate("", xy=(0.11, 16), xytext=(0.04, 16), arrowprops=dict(arrowstyle="<->", color=ENCRE2, lw=0.8))
etiquette(ax, 0.066, 17.5, "cohérence = 1", ha="center", fontsize=7)
etiquette(ax, 0.16, 8, "Analyse spectrale Lormes 23/4/86\nsortie enregistrement graphique\n« gain 40 000 », filtre 18 s",
          va="top", fontsize=7, color=ENCRE2)
axe_frequences(ax, 0.0033, 1); ax.set_ylim(-60, 20); ax.set_ylabel("dB réf. 1 V$^2$/Hz")
ax.legend(loc="lower left")
sauver(fig, "fig-4-2-2a")
