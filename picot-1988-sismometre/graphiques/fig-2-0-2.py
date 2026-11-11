"""Fig. 2.0.2 — réponse d'un capteur sismique (oscillateur du 2e ordre, gain mécanique 1)."""
from style import *

r = np.logspace(-2, 2, 1200)
fig, (a1, a2) = figure(6.3, 5.2, nrows=2, sharex=True)
for xi, c, ls, nom in [(0.05, ORANGE, "-", r"$\xi = 0{,}05$"), (0.707, BLEU, "-", r"$\xi = 0{,}707$")]:
    d = np.abs(1 - r**2 + 2j * xi * r)
    a1.plot(r, 20 * np.log10(1 / d), color=c, ls=ls, label=nom)
    a2.plot(r, 20 * np.log10(r**2 / d), color=c, ls=ls, label=nom)
a1.plot(r, np.where(r < 1, 0, -40 * np.log10(r)), color=GRIS, ls="--", lw=1)
a2.plot(r, np.where(r < 1, 40 * np.log10(r), 0), color=GRIS, ls="--", lw=1)
etiquette(a1, 6, -25, "asymptote\n$-40$ dB/décade", color=ENCRE2)
etiquette(a2, 0.035, -45, "asymptote\n$+40$ dB/décade", color=ENCRE2)
a1.set_ylabel(r"$|x/\ddot z_e| = |H_m(j\omega)|$ (dB)")
a2.set_ylabel(r"$|x/z_e|$ (dB)")
for a in (a1, a2):
    a.set_xscale("log"); axe_log(a); a.set_ylim(-80, 30)
    a.set_yticks(range(-80, 31, 20))
a2.set_xticks([0.01, 0.1, 1, 10, 100])
a2.set_xticklabels([r"$0{,}01\,f_m$", r"$0{,}1\,f_m$", r"$f_m$", r"$10\,f_m$", r"$100\,f_m$"])
a2.set_xlabel("Fréquence (normalisée à la fréquence propre $f_m$)")
a1.legend(loc="lower left")
sauver(fig, "fig-2-0-2")
