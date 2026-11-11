"""Fig. 2.1.9 — voir fig-2-1-8.py (même calcul, lame L = 185 mm).

-dM/dphi = Z^T J Z + [F_y, -F_x, 0] Z,  Z = [Y_Omega - Y_K, X_K - X_Omega, 1]  (m)
J : matrice jacobienne des efforts (p. 50 pour L = 186 mm, annexe 1.2 pour L = 185 mm).
Repère : origine à l'encastrement fixe O, K en (-132, 4) mm, pivot nominal en (-59, 24) mm.
"""
import sys
from style import *

CAS = {
    "fig-2-1-8": dict(L=186, J=[[381.144, -9.856, -12.0416], [-10.0024, 74.664, 3.2070], [-12.05, 3.1967, 0.67910]],
                      F=(-4.159098, 0.297250)),
    "fig-2-1-9": dict(L=185, J=[[398.412, -10.34, -12.37829], [-9.990, 77.70, 3.25553], [-12.384, 3.245, 0.6883]],
                      F=(-4.483739, 0.30936)),
}
XK, YK = -0.132, 0.004
NIVEAUX = [(-1.59e-2, "−2", ":", ORANGE), (0.0, "∞", "--", GRIS), (1.59e-2, "2", "-", BLEU), (6.35e-2, "1", "-", AQUA)]


def tracer(nom):
    c = CAS[nom]; J = np.array(c["J"]); Fx, Fy = c["F"]
    x = np.linspace(-0.135, 0.005, 700); y = np.linspace(-0.025, 0.075, 500)
    X, Y = np.meshgrid(x, y)
    z0, z1 = Y - YK, XK - X
    q = (J[0, 0] * z0 * z0 + (J[0, 1] + J[1, 0]) * z0 * z1 + J[1, 1] * z1 * z1
         + (J[0, 2] + J[2, 0]) * z0 + (J[1, 2] + J[2, 1]) * z1 + J[2, 2])
    moins_dM = q + Fy * z0 - Fx * z1
    fig, ax = figure(6.3, 3.9)
    lame = lire_csv("deformee-lame-experience")
    if lame is not None:
        ax.plot(lame["x_mm"], lame["y_mm"], color=ENCRE2, lw=1.0, label="lame déformée")
    for niv, lab, ls, col in NIVEAUX:
        cs = ax.contour(X * 1e3, Y * 1e3, moins_dM, levels=[niv], colors=[col], linestyles=[ls], linewidths=1.3)
        ax.plot([], [], color=col, ls=ls, label=f"courbe {lab}")
        # étiquette au point le plus à droite du contour
        segs = [s for s in cs.allsegs[0] if len(s)]
        if segs:
            s = max(segs, key=len); i = np.argmax(s[:, 0])
            etiquette(ax, s[i, 0] + 1.5, s[i, 1], lab, va="center")
    ax.plot([-59], [24], marker="o", ms=5, color=ENCRE, ls="none", label="pivot nominal $\\Omega$")
    ax.plot([XK * 1e3, 0], [YK * 1e3, 0], marker="s", ms=4, color=ENCRE2, ls="none")
    etiquette(ax, XK * 1e3 + 2, YK * 1e3 - 6, "$K$"); etiquette(ax, 1.5, -6, "$O$")
    ax.set_xlim(-135, 5); ax.set_ylim(-25, 75); ax.set_aspect("equal")
    ax.set_xlabel("$X_\\Omega$ (mm)"); ax.set_ylabel("$Y_\\Omega$ (mm)")
    ax.set_title(f"$L = {c['L']}$ mm", loc="right")
    ax.legend(loc="upper left", ncol=3)
    sauver(fig, nom)


tracer("fig-2-1-9")
