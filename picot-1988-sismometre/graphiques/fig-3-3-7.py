"""Fig. 3.3.7 — bruit équivalent en entrée selon la fréquence et le niveau d'excitation (tableau p. 168)."""
from style import *

# (excitation dBV_RMS, bruit asymptotique à 100 s, bruit réel à 10 s), dB réf. 1 m/√Hz
D = {"3,9 kHz": [(5.2, -203.5, -210.5), (12.9, -202, -213)],
     "7,8 kHz": [(13.9, -207.5, -215.5), (17.7, -204.5, -215.5)]}
fig, ax = figure(4.6, 3.2)
for (f, pts), c in zip(D.items(), (BLEU, ORANGE)):
    p = np.array(pts)
    ax.plot(p[:, 0], p[:, 1], "-o", color=c, ms=5, label=f"{f} — asymptotique à 100 s")
    ax.plot(p[:, 0], p[:, 2], "--s", color=c, ms=5, label=f"{f} — réel à 10 s")
ax.set_xlabel("Excitation (dBV$_{RMS}$)"); ax.set_ylabel("Bruit équivalent (dB réf. 1 m/$\\sqrt{\\mathrm{Hz}}$)")
ax.set_xlim(3, 20); ax.set_ylim(-218, -199)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7)
sauver(fig, "fig-3-3-7")
