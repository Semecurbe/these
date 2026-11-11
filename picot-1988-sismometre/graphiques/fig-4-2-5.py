"""Fig. 4.2.5 — observation de la marée terrestre, sortie « continu » gain 1000 accélération
(enregistrements numérisés, p. 178). Original : défilement 1,566 carreau/heure, 1 carreau =
0,5 µm s⁻² ; tirage réduit à 0,36 (carreau mesuré : 13,66 unités de page)."""
from style import *

CARREAU = 13.66
fig, axs = figure(6.3, 5.0, nrows=3, sharex=True)
noms = ["voie horizontale 1", "voie horizontale 2", "voie verticale (Z)"]
for k, ax in enumerate(axs, start=1):
    x, y = enregistrement("enregistrement-4-2-5", k)
    t, a = (x - 22) / CARREAU / 1.566, y / CARREAU * 0.5
    ax.plot(t, a, color=[BLEU, ORANGE, AQUA][k - 1], lw=0.9)
    if k == 2:  # tracé en butée (bas de bande) sur l'original
        i = np.flatnonzero(np.isnan(t))
        for j in i:
            ax.plot([t[j - 1], t[j + 1]], [np.nanmin(a)] * 2, color=ORANGE, lw=0.9, ls=":")
        etiquette(ax, 14, np.nanmin(a) + 0.08, "tracé en butée", fontsize=7, color=ENCRE2)
    ax.set_title(noms[k - 1], loc="left"); ax.set_ylabel("µm s$^{-2}$")
axs[-1].set_xlabel("Temps (h)")
fig.align_ylabels(axs)
sauver(fig, "fig-4-2-5")
