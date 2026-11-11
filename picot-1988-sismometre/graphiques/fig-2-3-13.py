"""Fig. 2.3.13 — bruit (densité spectrale) et dynamique maximale de quelques sismomètres (p. 118).

Deux grandeurs d'unités différentes : on les trace en deux panneaux superposés, même axe des
périodes (signal en dB réf. 1 m s⁻² RMS ; bruit en dB réf. 1 m s⁻²/√Hz)."""
from style import *

T = np.logspace(-2, 3, 400)
fig, (a1, a2) = figure(6.3, 6.4, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[1, 1.3]))
dyn = lire_courbes("dynamique-fig-2-3-1")
cols = {"ZM 500 — 7,2·10⁵ V/(m s⁻¹)": (BLEU, "-"), "ZM 500 — 1400 V/(m s⁻¹)": (BLEU, "--"),
        "LPH-A / LPZ-A (sortie V1)": (AQUA, "-"), "LPZ-12 s (correcteur 60 s)": (ORANGE, "-")}
for nom, (c, ls) in cols.items():
    d = dyn[nom]; a1.plot(d[:, 0], d[:, 1], color=c, ls=ls, label=texte(nom))
for nom in ("mb = 6,9 (Δ = 20°)", "Ms = 8,5 (Δ = 20°)"):
    d = dyn[nom]; a1.plot(d[:, 0], d[:, 1], color=GRIS, lw=0.9, ls=":")
    etiquette(a1, d[1, 0] * 1.1, d[1, 1], nom.replace("mb", "$m_b$").replace("Ms", "$M_s$"), fontsize=7, va="top")
a1.set_ylim(-110, -15); a1.set_ylabel("Signal max. (dB réf. 1 m s$^{-2}$)")
a1.legend(loc="lower right", fontsize=7)
bruits_reference(a2, lajitas=False, qcaz=False)
br = lire_courbes("bruit-fig-2-3-13")
for nom, c in [("ZM 500", BLEU), ("LPZ-12 s", ORANGE), ("LPH-A", AQUA)]:
    d = br[f"{nom} (électronique)"]; a2.plot(d[:, 0], d[:, 1], color=c, label=f"{nom} : électronique")
for nom, c, v in [("ZM 500 : Johnson ($\\xi_d$ = 0,707, $M$ = 0,7 kg, $T_m$ = 1 s)", BLEU, -187.5),
                  ("LPZ-12 s : Johnson ($\\xi_d$ = 0,707, $M$ = 2 kg, $T_m$ = 12 s)", ORANGE, -202.5),
                  ("LPH-A : Johnson ($\\xi_d$ = 0,01, $M$ = 2 kg, $T_m$ = 12 s)", AQUA, -220)]:
    a2.axhline(v, color=c, ls=(0, (1.5, 1.5)), lw=1.3, label=texte(nom))
a2.set_ylim(-226, -100); a2.set_ylabel("Bruit (dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$)")
axe_periodes(a2)
a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=7)
sauver(fig, "fig-2-3-13")
