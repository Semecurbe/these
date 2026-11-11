"""Approximation de 1/|Z_c| (branche de contre-réaction : R_f // C_f en série avec R_b)."""
from style import *

Rb, Rf, Tf = 100.0, 150e3, 1.4
Cf = Tf / (2 * np.pi * Rf)
w = np.logspace(-2, 6, 1500); s = 1j * w
Y = (1 + s * Rf * Cf) / (Rf + Rb * (1 + s * Rf * Cf))
wf, wb = 1 / (Rf * Cf), (Rb + Rf) / (Rf * Rb * Cf)
fig, ax = figure(5.6, 3.2)
ax.loglog(w, np.abs(Y), color=BLEU)
for x in (wf, wb): ax.axvline(x, color=ENCRE2, lw=0.6)
etiquette(ax, 0.015, 1.5 / (Rf + Rb), "$\\dfrac{1}{R_f + R_b}$"); etiquette(ax, 2e5, 1.5 / Rb, "$\\dfrac{1}{R_b}$", ha="center")
ax.set_xticks([wf, wb]); ax.set_xticklabels(["$\\dfrac{2\\pi}{T_f} = \\dfrac{1}{R_f C_f}$", "$\\dfrac{2\\pi}{T_b} = \\dfrac{R_b + R_f}{R_f R_b C_f}$"])
ax.set_xlabel("$\\omega$ (rad/s)"); ax.set_ylabel("$1/|Z_c|$ (S)"); ax.set_ylim(2e-6, 5e-2)
sauver(fig, "fig-3-2-zc")
