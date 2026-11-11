"""Fig. 2.2.3 — gain de boucle L(f) du sismomètre asservi : Bode et lieu de Nyquist.
T_m = 12 s, xi_m = 0,05, L(0) = 143, T_D = 2*pi*tau_D = 1,41 s (d'où T_0 = 1 s, xi_0 ~ 0,7)."""
from style import *

Tm, xim, L0, tauD = 12.0, 0.05, 143.0, 1.41 / (2 * np.pi)
wm = 2 * np.pi / Tm


def L(w):
    return L0 * wm**2 * (1 + 1j * w * tauD) / (wm**2 - w**2 + 2j * xim * wm * w)


f = np.logspace(-3, 1.3, 3000); Lf = L(2 * np.pi * f)
fig = plt.figure(figsize=(6.6, 5.6))
g = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], hspace=0.3, wspace=0.32)
am, ap = fig.add_subplot(g[0, 0]), fig.add_subplot(g[1, 0])
an, az = fig.add_subplot(g[0, 1]), fig.add_subplot(g[1, 1])
am.plot(f, 20 * np.log10(np.abs(Lf)), color=BLEU)
am.axhline(0, color=ENCRE2, lw=0.7)
etiquette(am, 0.25, 32, "$-40$ dB/déc."); etiquette(am, 1.6, -5, "$-20$ dB/déc.")
etiquette(am, 0.0012, -30, "$T_m = 12$ s\n$\\xi_m = 0{,}05$\n$L(0) = 143$", color=ENCRE2)
am.set_ylabel("Module $|L|$ (dB)"); am.set_ylim(-40, 70)
ap.plot(f, np.degrees(np.unwrap(np.angle(Lf))), color=BLEU)
ap.set_ylabel("Phase de $L$ (degrés)"); ap.set_ylim(-190, 10); ap.set_yticks([0, -90, -180])
ap.set_xlabel("Fréquence (Hz)")
for a in (am, ap):
    a.set_xscale("log"); axe_log(a); a.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
# lieu de Nyquist global
an.plot(Lf.real, Lf.imag, color=BLEU)
for T in [20, 15, 14, 13, 12, 10, 8]:
    p = L(2 * np.pi / T); an.plot(p.real, p.imag, "o", ms=3, color=ENCRE)
    etiquette(an, p.real, p.imag, f" {T} s", fontsize=7)
an.plot([-1], [0], "+", color=ORANGE, ms=8, mew=1.5)
an.set_xlabel("Partie réelle"); an.set_ylabel("Partie imaginaire"); an.set_title("lieu de $L(j\\omega)$", loc="right")
an.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
an.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
# détail au voisinage du point critique
m = (np.abs(Lf) < 4)
az.plot(Lf.real[m], Lf.imag[m], color=BLEU)
for T in [1.2, 1, 0.7, 0.5, 0.1]:
    p = L(2 * np.pi / T); az.plot(p.real, p.imag, "o", ms=3, color=ENCRE)
    etiquette(az, p.real, p.imag, f"  {format_nombre(T)} s", fontsize=7, va="center")
az.plot([-1], [0], "+", color=ORANGE, ms=9, mew=1.6)
etiquette(az, -1, 0.15, "point\ncritique", ha="center", fontsize=7)
az.axhline(0, color=ENCRE2, lw=0.6); az.axvline(0, color=ENCRE2, lw=0.6)
az.set_xlim(-2.2, 0.6); az.set_ylim(-2.6, 0.5); az.set_aspect("equal")
az.set_xlabel("Partie réelle"); az.set_title("détail : voisinage de $-1$", loc="right")
az.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
az.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_nombre))
sauver(fig, "fig-2-2-3")
