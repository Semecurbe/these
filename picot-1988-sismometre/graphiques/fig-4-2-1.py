"""Fig. 4.2.1 — comparaison des sismomètres LDG LPZ-A et LPZ-12 s : sortie vitesse, gain 40 000,
bande 18–60 s (enregistrements numérisés, p. 173). Échelles de l'original : 1 carreau = 20 s
(horizontal) et 12,5 µm dans la bande (vertical) ; carreau mesuré : 5,65 unités de page."""
from style import *

CARREAU = 5.65
fig, axs = figure(6.3, 5.6, nrows=4, sharex=True)
titres = ["Période calme", None, "Séisme", None]
for k, ax in enumerate(axs, start=1):
    x, y = enregistrement("enregistrement-4-2-1", k)
    t = (x - 68) / CARREAU * 20
    ax.plot(t, y / CARREAU * 12.5, color=BLEU if k % 2 else ORANGE, lw=0.7)
    ax.set_ylim(-45, 45); ax.set_yticks([-25, 0, 25])
    if titres[k - 1]:
        ax.set_title(titres[k - 1], loc="left")
    ax.set_ylabel("µm")
axs[-1].set_xlabel("Temps (s)"); axs[-1].set_xlim(0, (797 - 68) / CARREAU * 20)
fig.align_ylabels(axs)
sauver(fig, "fig-4-2-1")
