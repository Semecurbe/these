"""Fig. 5.1.4 — signaux maximaux et bruits des voies V1 et V2 du sismomètre mixte (p. 190).
Signal et bruit ont des unités différentes : deux panneaux, même axe des périodes."""
from style import *

c = lire_courbes("mixte-fig-5-1-4")
fig, (a1, a2) = figure(6.3, 5.8, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[1, 1.5]))
for nom, col, ls in [("V1 : sortie accélération « gain 10 »", BLEU, "-"), ("V2 : sortie 10⁴ V/(m s⁻¹)", ORANGE, "--"),
                     ("V2 : sortie 10⁶ V/(m s⁻¹)", ORANGE, "-")]:
    d = c[nom]; a1.plot(d[:, 0], d[:, 1], color=col, ls=ls, label=texte(nom))
a1.set_ylim(-95, -15); a1.set_ylabel("Signal max. (dB réf. 1 m s$^{-2}$)"); a1.legend(loc="lower right", fontsize=7)
bruits_reference(a2, lajitas=False, qcaz=False)
for nom, col, ls in [("V1 : bruit blanc et bruit excédentaire LVDT", BLEU, "-"), ("V2 : bruit propre", ORANGE, "--"),
                     ("V2 : bruit réjecté par V1", ORANGE, "-"), ("Bruit de Johnson", GRIS, "-.")]:
    d = c[nom]; a2.plot(d[:, 0], d[:, 1], color=col, ls=ls, label=texte(nom))
a2.set_ylim(-226, -95); a2.set_ylabel("Bruit (dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$)")
axe_periodes(a2)
a2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=7)
sauver(fig, "fig-5-1-4")
