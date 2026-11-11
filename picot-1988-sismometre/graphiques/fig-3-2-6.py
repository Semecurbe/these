"""Fig. 3.2.6 — analyses spectrales, LVDT bloqué : A — LVDT faible bruit ; B — LVDT standard (p. 152)."""
from style import *

fig, (a, b) = figure(6.3, 6.4, nrows=2)
spectre(a, "spectre-3-2-6A", color=BLEU)
axe_spectre(a); a.set_title("A — LVDT faible bruit", loc="left")
spectre(b, "spectre-3-2-6B", color=BLEU)
axe_spectre(b, 0.0035, 1, -60, 0); b.set_title("B — LVDT standard", loc="left")
etiquette(b, 0.13, -3, "LVDT Schaevitz 050 HR standard\nfiltre de sortie passe-bas 9 s\nsortie gain 1000 accélération\n"
          "excitation 4 V$_{cc}$, $f_e$ = 1 kHz\ngain de tête = 200", va="top", fontsize=7, color=ENCRE2)
fig.tight_layout()
sauver(fig, "fig-3-2-6")
