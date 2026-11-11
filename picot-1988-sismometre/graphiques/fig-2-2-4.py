"""Fig. 2.2.4 — réponse en accélération du sismomètre à équilibre de force (T_m = 12 s, T_0 = 1 s)."""
from style import *

Tm, xim, T0, xi0 = 12.0, 0.05, 1.0, 0.707
wm, w0 = 2 * np.pi / Tm, 2 * np.pi / T0
f = np.logspace(-3, 1.5, 1500); w = 2 * np.pi * f
ouv = 1 / np.abs(wm**2 - w**2 + 2j * xim * wm * w)
fer = 1 / np.abs(w0**2 - w**2 + 2j * xi0 * w0 * w)
ref = 1 / w0**2
fig, ax = figure(6.0, 3.6)
ax.plot(f, 20 * np.log10(ouv / ref), color=ORANGE, label="oscillations libres sans contre-réaction")
ax.plot(f, 20 * np.log10(fer / ref), color=BLEU, label="réponse avec contre-réaction")
ax.annotate("", xy=(1 / T0, -3), xytext=(1 / T0, 0), arrowprops=dict(arrowstyle="<->", color=ENCRE2, lw=0.8))
etiquette(ax, 1.15 / T0, -2.5, "3 dB")
etiquette(ax, 3, -35, "déplacement\n$-40$ dB/décade", color=ENCRE2)
for x in (1 / Tm, 1 / T0):
    ax.axvline(x, color=ENCRE2, lw=0.6)
ax.set_xscale("log"); axe_log(ax)
ax.set_xticks([1 / Tm, 1 / T0]); ax.set_xticklabels(["$f_m$", "$f_0$"])
ax.set_ylim(-60, 75); ax.set_xlabel("Fréquence (log)"); ax.set_ylabel("$|V_0/\\gamma_i|$ (dB, réf. gain asservi)")
ax.legend(loc="upper right")
sauver(fig, "fig-2-2-4")
