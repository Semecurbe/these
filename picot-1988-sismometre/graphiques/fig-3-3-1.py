"""Fig. 3.3.1 — LVDT Schaevitz 050 HR standard : bruit ramené en entrée à 10 s (dB réf. 1 m/√Hz)
selon la fréquence et le niveau d'excitation (relevé de l'original, p. 156)."""
from style import *

# (fréquence kHz, excitation V_cc, bruit dB)
P = [(1, 4, -178), (2.4, 0.12, -185), (2.4, 0.4, -185), (2.4, 1.2, -185), (2.4, 4, -181),
     (5, 1.2, -185), (5, 4, -185), (9.6, 1.2, -183.5)]
fig, ax = figure(5.4, 3.0)
for f, v, b in P:
    c = BLEU if b <= -185 else (ORANGE if b > -182 else AQUA)
    ax.plot(v, f, "o", ms=7, color=c)
    etiquette(ax, v * 1.12, f, f"{format_nombre(b)}", va="center")
ax.set_xscale("log"); ax.set_xlim(0.08, 12)
ax.set_xticks([0.12, 0.4, 1.2, 4, 10]); ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_ylim(10.5, 0); ax.set_yticks([1, 2.4, 5, 9.6]); ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
sec = ax.secondary_xaxis("top", functions=(lambda v: v / (2 * np.sqrt(2)), lambda r: r * 2 * np.sqrt(2)))
sec.set_xticks([0.1, 1]); sec.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre)); sec.set_xlabel("($V_{RMS}$)")
ax.set_xlabel("Niveau d'excitation ($V_{cc}$)"); ax.set_ylabel("Fréquence d'excitation (kHz)")
ax.grid(which="minor", visible=False)
sauver(fig, "fig-3-3-1")
