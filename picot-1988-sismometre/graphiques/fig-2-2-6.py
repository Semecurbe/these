"""Fig. 2.2.6 — admittance de conversion tension-courant (R_b = 100 ohm, R_f = 150 kohm, C_f = 1,5 µF)."""
from style import *

Rb, Rf, Cf = 100.0, 150e3, 1.5e-6
Rp = Rf * Rb / (Rf + Rb)
f = np.logspace(-3, 5, 1500); s = 2j * np.pi * f
Y = (1 + s * Rf * Cf) / ((Rf + Rb) * (1 + s * Rp * Cf))
fD, fD2 = 1 / (2 * np.pi * Rf * Cf), 1 / (2 * np.pi * Rp * Cf)
fig, ax = figure(6.0, 3.4)
ax.loglog(f, np.abs(Y), color=BLEU)
ax.loglog(f, np.clip(1 / (Rf + Rb) * f / fD, 1 / (Rf + Rb), 1 / Rb), color=GRIS, ls="--", lw=1)
for x in (fD, fD2):
    ax.axvline(x, color=ENCRE2, lw=0.6)
etiquette(ax, fD * 1.15, 2e-6, "$f_D = \\dfrac{1}{2\\pi R_f C_f} \\approx 0{,}71$ Hz")
etiquette(ax, fD2 / 1.15, 2e-6, "$f'_D = \\dfrac{1}{2\\pi (R_f /\\!/ R_b) C_f} \\approx 1$ kHz", ha="right")
etiquette(ax, 2e-3, 1.4 / (Rf + Rb), "$1/(R_f+R_b)$"); etiquette(ax, 2e4, 1.4 / Rb, "$1/R_b$", ha="center")
ax.set_xlabel("Fréquence (Hz)"); ax.set_ylabel("$|Y|$ (S)"); ax.set_ylim(2e-7, 5e-2)
sauver(fig, "fig-2-2-6")
