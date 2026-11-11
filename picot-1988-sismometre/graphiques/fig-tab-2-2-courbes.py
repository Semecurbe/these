"""Courbes de réponse du tableau « théorie simplifiée du sismomètre asservi » (§ 2.2.1)."""
# sorties: tab-2-2-courbe1, tab-2-2-courbe2
from style import *

Tm, xim, tauD = 12.0, 0.05, 1.41 / (2 * np.pi)
f = np.logspace(-3, 2, 1000); w = 2 * np.pi * f; wm = 2 * np.pi / Tm
# suspension mécanique
fig, ax = figure(3.1, 2.5)
ax.plot(f, 20 * np.log10(wm**2 / np.abs(wm**2 - w**2 + 2j * xim * wm * w)), color=BLEU)
ax.plot(f, np.where(f < 1 / Tm, 0, -40 * np.log10(f * Tm)), color=GRIS, ls="--", lw=1)
ax.axvline(1 / Tm, color=ENCRE2, lw=0.6)
etiquette(ax, 0.3, -30, "$-40$ dB/décade")
ax.set_xscale("log"); axe_log(ax); ax.set_ylim(-110, 30)
ax.set_xticks([1 / Tm]); ax.set_xticklabels(["$\\omega_m/2\\pi$"])
ax.set_ylabel("$|x_G/\\gamma_i|$ (dB)"); ax.set_xlabel("$f$")
sauver(fig, "tab-2-2-courbe1")
# contre-réaction P + D
fig, ax = figure(3.1, 2.5)
ax.plot(f, 20 * np.log10(np.abs(1 + 1j * w * tauD)), color=BLEU)
fc = 1 / (2 * np.pi * tauD)
ax.plot(f, np.where(f < fc, 0, 20 * np.log10(f / fc)), color=GRIS, ls="--", lw=1)
ax.axvline(fc, color=ENCRE2, lw=0.6)
etiquette(ax, 0.02, 25, "$+20$ dB/décade")
ax.set_xscale("log"); axe_log(ax); ax.set_ylim(-5, 45)
ax.set_xticks([fc]); ax.set_xticklabels(["$1/2\\pi\\tau_D$"])
ax.set_ylabel("$|\\gamma_f/U|$ (dB réf. $\\beta_0$)"); ax.set_xlabel("$f$")
sauver(fig, "tab-2-2-courbe2")
