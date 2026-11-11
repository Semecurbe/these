"""Fig. 5.1.2 et 5.1.3 — courbes de réponse et signal maximum admissible du sismomètre mixte (T_0 = 1 s)."""
# sorties: fig-5-1-2, fig-5-1-3
from style import *

T = np.logspace(-2, 2, 800); T0, xi0 = 1.0, 0.707
w, w0 = 2 * np.pi / T, 2 * np.pi / T0
D = np.abs(w0**2 - w**2 + 2j * xi0 * w0 * w)
H1, H2 = w0**2 / D, w0 * w / D
fig, (a1, a2) = figure(4.8, 4.2, nrows=2, sharex=True)
a1.loglog(T, H1, color=BLEU); a2.loglog(T, H2, color=BLEU)
for a in (a1, a2):
    a.axvline(T0, color=ENCRE2, lw=0.6); axe_log(a); axe_log(a, "y")
a1.set_ylabel("$|V_1/\\gamma_i|$"); a2.set_ylabel("$|V_2/\\gamma_i|$")
a2.set_xticks([T0]); a2.set_xticklabels(["$T_0$"]); a2.set_xlabel("Période $T$ (log)")
for a in (a1, a2): a.yaxis.set_major_formatter(NullFormatter())
sauver(fig, "fig-5-1-2")
# 5.1.3 : signal maximum admissible
g1 = 1 / H1; g2 = 3 / H2
fig, ax = figure(4.8, 2.8)
ax.loglog(T, g1, color=BLEU, label="$\\gamma_{Mad1} = V_{1Mad}/H_{i1}$")
ax.loglog(T, g2, color=ORANGE, ls="-.", label="$V_{2Mad}/H_{i2}$")
ax.axvline(T0, color=ENCRE2, lw=0.6); axe_log(ax); axe_log(ax, "y")
ax.set_xticks([T0]); ax.set_xticklabels(["$T_0$"]); ax.yaxis.set_major_formatter(NullFormatter())
ax.set_xlabel("Période $T$ (log)"); ax.set_ylabel("$|\\gamma_{Mad}|$"); ax.legend(loc="upper center")
sauver(fig, "fig-5-1-3")
