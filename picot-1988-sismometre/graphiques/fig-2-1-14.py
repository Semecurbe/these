"""Fig. 2.1.14 — constante de couple d'un élément de lame d'un pivot bi-lames (Weinstein, 1965).

En unités réduites : p = P L^2 / (E I) (p < 0 : compression), u = L*lambda = sqrt(|p|),
  compression : (M/Theta) / (EI/L) = (u/2) [u/2 + cotg(u/2)]
  traction    : (M/Theta) / (EI/L) = (u/2) [coth(u/2) - u/2]
(les deux branches valent 1 pour p = 0, c'est-à-dire EI/L).
"""
from style import *

pc = np.linspace(-38.5, -1e-6, 600); u = np.sqrt(-pc)
kc = (u / 2) * (u / 2 + 1 / np.tan(u / 2))
pt = np.linspace(1e-6, 38, 600); v = np.sqrt(pt)
kt = (v / 2) * (1 / np.tanh(v / 2) - v / 2)
fig, ax = figure(6.0, 3.6)
ax.plot(np.r_[pc, pt], np.r_[kc, kt], color=BLEU)
ax.axhline(0, color=ENCRE2, lw=0.7); ax.axvline(0, color=ENCRE2, lw=0.7)
ax.set_xlim(-40, 40); ax.set_ylim(-7, 7)
ax.set_xlabel("Charge unitaire $P\\,L^2/(E I)$"); ax.set_ylabel("Constante de couple ($E I / L$)")
etiquette(ax, -25, -5, "COMPRESSION", ha="center", color=ENCRE2)
etiquette(ax, 22, 4, "TRACTION", ha="center", color=ENCRE2)
sauver(fig, "fig-2-1-14")
