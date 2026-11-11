"""Fig. 2.1.5 (bas) — cheminement retenu pour obtenir la géométrie déformée de la lame
(étapes A, B, C ; relevé de l'original p. 39, recalé sur K' = −132 mm et O = 0)."""
from style import *

c = lire_courbes("lame-etapes", cle="etape")
k = 132 / (132 - 2.3 - 1.0)
fig, ax = figure(4.2, 4.6)
for nom, col, ls in [("A", ORANGE, "-"), ("B", AQUA, "--"), ("C", BLEU, "-")]:
    d = c[nom]; x = (d[:, 0] + 2.3) * k; y = d[:, 1]
    ax.plot(x, y, color=col, ls=ls, label=f"Étape {nom}")
ax.axvline(0, color=ENCRE2, lw=0.8)
ax.annotate("", xy=(-132, 120), xytext=(0, 120), arrowprops=dict(arrowstyle="<->", color=ENCRE2, lw=0.8))
etiquette(ax, -66, 122, "$U = -132$ mm", ha="center", va="bottom")
ax.annotate("", xy=(-122, 108), xytext=(-122, 33), arrowprops=dict(arrowstyle="-", color=ENCRE2, lw=0.8))
etiquette(ax, -120, 72, "$V = -182$ mm", rotation=90, va="center")
for (x, y, t) in [(-132, 114.5, "$K'$"), (-132, 3, "$K$"), (0, 0, "$O$")]:
    ax.plot(x, y, "o", ms=3.5, color=ENCRE); etiquette(ax, x + 2, y + 3, t)
etiquette(ax, -118, 0, "$\\theta_K = 180°$", fontsize=7)
ax.set_xlim(-145, 8); ax.set_ylim(-10, 170); ax.set_aspect("equal")
ax.set_xlabel("$x$ (mm)"); ax.set_ylabel("$y$ (mm)"); ax.legend(loc="upper right")
sauver(fig, "fig-2-1-5b")
