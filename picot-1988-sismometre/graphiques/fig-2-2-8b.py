"""Fig. 2.2.8 (2) — réponse « large bande vitesse » d'un sismomètre sur-amorti (xi = 4)."""
from style import *

xi = 4.0
r = np.logspace(-3, 2, 1500)
H = 1 / np.abs(1 - r**2 + 2j * xi * r)
r1, r2 = xi - np.sqrt(xi**2 - 1), xi + np.sqrt(xi**2 - 1)
fig, ax = figure(6.0, 3.4)
ax.plot(r, 20 * np.log10(H), color=BLEU, label="sismomètre sur-amorti ($\\xi = 4$)")
ax.plot(r, np.where(r < 1, 0, -40 * np.log10(r)), color=GRIS, ls="--", lw=1, label="asymptotes du 2$^e$ ordre ($\\xi \\leq 1$)")
ax.axvline(1, color=ENCRE2, lw=0.6)
etiquette(ax, 0.02, -15, "$-20$ dB/décade"); etiquette(ax, 15, -62, "$-40$ dB/décade")
for x, t in [(0.004, "Accélération"), (0.6, "Vitesse"), (25, "Déplacement")]:
    etiquette(ax, x, -95, t, ha="center", color=ENCRE2)
ax.set_xscale("log"); axe_log(ax)
ax.set_xticks([r1, 1, r2]); ax.set_xticklabels(["$f_n/2\\xi$", "$f_n$", "$2\\xi f_n$"])
ax.set_ylim(-100, 8); ax.set_xlabel("Fréquence (log)"); ax.set_ylabel("$|V/\\gamma_i|$ (dB)")
ax.legend(loc="upper right")
sauver(fig, "fig-2-2-8b")
