"""Fig. 4.2.3 — analyses spectrales de bruit avec le sismomètre LPZ asservi (p. 176).
En haut : spectre mesuré (LPZ-A, relecture 27/4/86 17 h 30 – 22 h 10, sortie PCM gain 1000).
En bas : spectre ramené en accélération (spectre mesuré corrigé de la réponse de la chaîne,
fig. 4.2.4 — recalculé ici) comparé aux spectres de bruit sismique de référence."""
from style import *

fig, (a, b) = figure(6.3, 6.8, nrows=2)
d = np.genfromtxt(DONNEES / "spectre-4-2-3.csv", delimiter=",", names=True)
o = np.argsort(d["x"]); T, S = d["x"][o], d["y"][o]
a.plot(T, S, color=BLEU, lw=0.8)
axe_periodes(a, 1, 300); a.invert_xaxis(); a.set_ylim(-80, -10); a.set_ylabel("dB réf. 1 V$^2$/Hz")
a.set_title("LPZ-A — relecture des signaux 27/4/86, 17 h 30 – 22 h 10, sortie PCM gain 1000", loc="left", fontsize=8)
# correction par la réponse de la chaîne (dB réf. 1 V/(m s⁻²))
r = lire_courbes("reponse-fig-4-2-4")["réponse"]
G = np.interp(np.log10(T), np.log10(r[::-1, 0]), r[::-1, 1], left=np.nan, right=np.nan)
bruits_reference(b)
b.plot(T, S - G, color=BLEU, lw=0.8, label="Lormes (LPZ-A)")
axe_periodes(b); b.set_ylim(-220, -100); b.set_ylabel("dB réf. 1 m s$^{-2}$/$\\sqrt{\\mathrm{Hz}}$")
b.legend(loc="upper right", ncol=2, fontsize=7)
fig.tight_layout()
sauver(fig, "fig-4-2-3")
