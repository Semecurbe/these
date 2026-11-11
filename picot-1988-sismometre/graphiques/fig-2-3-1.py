"""Fig. 2.3.1 — signaux maximaux admissibles : capteur électrodynamique et capteur asservi (p. 91)."""
from style import *

fig, ax = figure(6.3, 3.8)
dyn = lire_courbes("dynamique-fig-2-3-1")
cols = {"ZM 500 — 7,2·10⁵ V/(m s⁻¹)": (BLEU, "-"), "ZM 500 — 1400 V/(m s⁻¹)": (BLEU, "--"),
        "LPH-A / LPZ-A (sortie V1)": (AQUA, "-"), "LPZ-12 s (correcteur 60 s)": (ORANGE, "-")}
for nom, (c, ls) in cols.items():
    d = dyn[nom]; ax.plot(d[:, 0], d[:, 1], color=c, ls=ls, label=texte(nom))
for nom in ("mb = 6,9 (Δ = 20°)", "Ms = 8,5 (Δ = 20°)"):
    d = dyn[nom]; ax.plot(d[:, 0], d[:, 1], color=GRIS, lw=0.9, ls=":")
    etiquette(ax, d[1, 0] * 1.1, d[1, 1], nom.replace("mb", "$m_b$").replace("Ms", "$M_s$"), fontsize=7, va="top")
# droites d'iso-déplacement (pente +40 dB/décade), en arrière-plan
T = np.logspace(-2, 3, 50)
for k in range(-14, 3):
    ax.plot(T, 40 * np.log10(T) + 10 * k * 2, color=GRILLE, lw=0.5, zorder=0)
etiquette(ax, 8, -100, "Accélération", color=ENCRE2); etiquette(ax, 150, -95, "Déplacement\n(+40 dB/déc.)", color=ENCRE2)
axe_periodes(ax); ax.set_ylim(-120, -20)
ax.set_ylabel("dB réf. 1 m s$^{-2}$ RMS")
ax.legend(loc="lower left", fontsize=7)
sauver(fig, "fig-2-3-1")
