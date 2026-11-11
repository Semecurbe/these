"""Fig. 4.2.6 — comparaison avec un capteur GEOSCOPE, composante Z, bande 150–3600 s
(enregistrements numérisés, p. 180). Échelles de l'original : 1 heure = 12 carreaux,
1 cm = 2 carreaux (photocopie réduite à 72 % ; carreau mesuré : 13,8 unités de page) ;
sensibilités S = 1 200 000 mm/(m s⁻²) (LDG) et 1 344 000 mm/(m s⁻²) (GEOSCOPE)."""
from style import *

CARREAU = 13.8
fig, axs = figure(6.3, 3.8, nrows=2, sharex=True, sharey=True)
for k, (ax, nom, S, c) in enumerate(zip(axs, ["Z — LPZ-A (LDG)", "Z — GEOSCOPE"], [1.2e6, 1.344e6], [BLEU, ORANGE]), start=1):
    x, y = enregistrement("enregistrement-4-2-6", k)
    mm = y / (2 * CARREAU) * 10                    # millimètres sur l'enregistreur
    ax.plot((x - 27) / CARREAU / 12, mm / S * 1e6, color=c, lw=0.8)   # µm s⁻²
    ax.set_title(nom, loc="left"); ax.set_ylabel("µm s$^{-2}$")
axs[-1].set_xlabel("Temps (h)")
sauver(fig, "fig-4-2-6")
