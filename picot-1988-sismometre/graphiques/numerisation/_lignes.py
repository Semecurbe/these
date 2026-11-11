import sys, numpy as np
from outils import page, K
def lignes(n, box, frac=0.5, rot=0):
    im = page(n, rot); x0,y0,x1,y1 = [int(v*K) for v in box]
    a = im[y0:y1, x0:x1] < 150
    def grp(v):
        idx = np.flatnonzero(v); out=[]
        for i in idx:
            if out and i-out[-1][-1] <= 2: out[-1].append(i)
            else: out.append([i])
        return [round(np.mean(g)/K + o, 1) for g, o in [(g, 0) for g in out]]
    vx = [round(v + x0/K, 1) for v in grp(a.mean(0) > frac)]
    vy = [round(v + y0/K, 1) for v in grp(a.mean(1) > frac)]
    return vx, vy
for spec in sys.argv[1:]:
    n, b = spec.split(":"); box = [float(v) for v in b.split(",")]
    vx, vy = lignes(int(n), box)
    print(f"p{n} V: {vx}\n     H: {vy}")
