"""Fig. 2.2.1 (courbe) — réponse en accélération du sismomètre électrodynamique (sortie vitesse)."""
from style import *

r = np.logspace(-2, 2, 1200)
fig, ax = figure(6.0, 3.4)
for xi, c, nom in [(0.02, ORANGE, "réponse non amortie ($R_{am}\\to\\infty$)"), (0.707, BLEU, "réponse optimum ($\\xi = 0{,}707$)")]:
    ax.plot(r, 20 * np.log10(r / np.abs(1 - r**2 + 2j * xi * r)), color=c, label=nom)
ax.plot(r, np.where(r < 1, 20 * np.log10(r), -20 * np.log10(r)), color=GRIS, ls="--", lw=1, label="asymptotes ($\\pm 20$ dB/décade)")
ax.annotate("", xy=(1, -3), xytext=(1, 0), arrowprops=dict(arrowstyle="<->", color=ENCRE2, lw=0.8))
etiquette(ax, 1.15, -2.2, "3 dB")
ax.annotate("", xy=(100, -48), xytext=(1.05, -48), arrowprops=dict(arrowstyle="->", color=ENCRE2, lw=0.8))
etiquette(ax, 1.3, -46, "mesure de la vitesse du sol ($f > f_n$)", color=ENCRE2)
ax.set_xscale("log"); axe_log(ax); ax.set_ylim(-52, 40)
ax.set_xticks([0.01, 0.1, 1, 10, 100]); ax.set_xticklabels(["$0{,}01\\,f_n$", "$0{,}1\\,f_n$", "$f_n$", "$10\\,f_n$", "$100\\,f_n$"])
ax.set_xlabel("Fréquence (log)"); ax.set_ylabel("$|V_0/\\gamma_i|$ (dB, référence arbitraire)")
ax.legend(loc="upper left")
sauver(fig, "fig-2-2-1b")
