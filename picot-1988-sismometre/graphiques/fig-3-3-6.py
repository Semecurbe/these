"""Fig. 3.3.6 — influence de la fréquence d'excitation sur les analyses spectrales (p. 167)."""
from style import *

fig, (a, b) = figure(6.3, 6.6, nrows=2, sharex=True)
for ax, nom, titre, (h, l) in [(a, "spectre-3-3-6a", "$f_e$ = 3,9 kHz — gain de tête 54 dB", ("12,9", "5,2")),
                               (b, "spectre-3-3-6b", "$f_e$ = 7,8 kHz — gain de tête 52,7 dB", ("17,7", "13,9"))]:
    spectre(ax, f"{nom}-haut", color=ORANGE, label=f"excitation {h} dBV$_{{RMS}}$")
    spectre(ax, f"{nom}-bas", color=BLEU, label=f"excitation {l} dBV$_{{RMS}}$")
    axe_spectre(ax); ax.set_title(titre, loc="left"); ax.legend(loc="lower left")
a.set_xlabel("")
fig.tight_layout()
sauver(fig, "fig-3-3-6")
