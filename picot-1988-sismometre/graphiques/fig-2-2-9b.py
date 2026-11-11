"""Fig. 2.2.9 (suite) — réponses asymptotiques des sorties LP et BRB du sismomètre PID à deux boucles."""
from style import *

f = np.logspace(-3, 1, 400); f1, f2 = 1 / 20, 1 / 0.2
w1 = 2 * np.pi * f1
lp = np.where(f < f1, 7600, 7600 * (f1 / f)); lp = np.where(f > f2, 7600 * (f1 / f2) * (f2 / f)**2, lp)
brb = np.where(f < f1, 7600 * (f / f1), 7600 * (f1 / f)); brb = np.where(f > f2, 7600 * (f1 / f2) * (f2 / f)**2, brb)
fig, (a1, a2) = figure(5.2, 4.6, nrows=2, sharex=True)
a1.loglog(f, lp, color=BLEU); a2.loglog(f, brb, color=BLEU)
for a in (a1, a2):
    for x in (f1, f2): a.axvline(x, color=ENCRE2, lw=0.6)
    axe_log(a); axe_log(a, "y")
etiquette(a1, 0.004, 9000, "$2 \\times 3800$ V/(m s$^{-2}$)")
etiquette(a1, 0.003, 1500, "accélération", color=ENCRE2); etiquette(a1, 0.35, 1500, "déplacement", color=ENCRE2)
etiquette(a2, f1 * 1.15, 9000, "$2 \\times 1200$ V/(m s$^{-1}$)")
etiquette(a2, 0.4, 200, "vitesse", color=ENCRE2)
a1.set_ylabel("$|V_{LP}/\\gamma_i|$"); a2.set_ylabel("$|V_{BRB}/\\gamma_i|$")
a1.set_ylim(30, 4e4); a2.set_ylim(5, 4e4)
a2.set_xticks([f1, f2]); a2.set_xticklabels(["20 s", "0,2 s"]); a2.set_xlabel("Fréquence (log) — périodes indiquées")
sauver(fig, "fig-2-2-9b")
