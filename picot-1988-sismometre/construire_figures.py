#!/usr/bin/env python3
"""Génère les figures de la thèse, en dehors de la compilation Quarto.

- schemas/fig-*.tex      : schémas TikZ (standalone)  -> figures/generees/<nom>.pdf + .svg
- graphiques/fig-*.py    : graphiques matplotlib      -> figures/generees/<nom>.pdf + .svg

Seules les figures dont la source (ou une dépendance commune) est plus récente
que la sortie sont reconstruites.

Usage :
    python3 construire_figures.py              # reconstruit ce qui est périmé
    python3 construire_figures.py --force      # reconstruit tout
    python3 construire_figures.py fig-2-0-1    # reconstruit certaines figures
"""
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RACINE = Path(__file__).resolve().parent
SCHEMAS = RACINE / "schemas"
GRAPHIQUES = RACINE / "graphiques"
SORTIE = RACINE / "figures" / "generees"
CONSTRUCTION = SCHEMAS / "_construction"


def trouver_latex():
    exe = shutil.which("pdflatex")
    if exe:
        return exe
    tinytex = Path.home() / ".TinyTeX" / "bin" / "x86_64-linux" / "pdflatex"
    if tinytex.exists():
        return str(tinytex)
    sys.exit("pdflatex introuvable (installer TinyTeX : quarto install tinytex)")


def perime(sortie: Path, dependances) -> bool:
    if not sortie.exists():
        return True
    t = sortie.stat().st_mtime
    return any(d.stat().st_mtime > t for d in dependances if d.exists())


def construire_tex(src: Path, latex: str) -> str:
    CONSTRUCTION.mkdir(exist_ok=True)
    cmd = [latex, "-interaction=nonstopmode", "-halt-on-error",
           f"-output-directory={CONSTRUCTION}", src.name]
    r = subprocess.run(cmd, cwd=SCHEMAS, capture_output=True, text=True)
    pdf = CONSTRUCTION / f"{src.stem}.pdf"
    if r.returncode != 0 or not pdf.exists():
        log = (CONSTRUCTION / f"{src.stem}.log")
        extrait = ""
        if log.exists():
            lignes = log.read_text(errors="replace").splitlines()
            idx = [i for i, l in enumerate(lignes) if l.startswith("!")]
            if idx:
                extrait = "\n".join(lignes[idx[0]:idx[0] + 6])
        return f"ÉCHEC {src.name}\n{extrait}"
    shutil.copy(pdf, SORTIE / f"{src.stem}.pdf")
    subprocess.run(["pdftocairo", "-svg", str(SORTIE / f"{src.stem}.pdf"),
                    str(SORTIE / f"{src.stem}.svg")], check=True)
    return f"ok   {src.name}"


def dependances_tex(src: Path):
    """Le schéma, le préambule et les fragments qu'il inclut (\\input{_...})."""
    deps = [src, SCHEMAS / "_preambule.tex"]
    for nom in re.findall(r"\\input\{(_[^}]+)\}", src.read_text()):
        deps.append(SCHEMAS / (nom if nom.endswith(".tex") else nom + ".tex"))
    return deps


def dependances_donnees(src: Path):
    """Fichiers de graphiques/donnees/ cités dans le script (directement ou via un préfixe)."""
    texte = src.read_text()
    prefixes = re.findall(r'"([a-z0-9-]+)', texte)
    if "bruits_reference" in texte:  # spectres de référence lus par style.py
        prefixes += ["bruit-iris-M", "bruit-iris-m", "bruit-qcaz", "bruit-lajitas"]
    return [f for f in (GRAPHIQUES / "donnees").glob("*.csv")
            if any(p and f.stem.startswith(p) and len(p) > 4 for p in prefixes)]


def sorties_py(src: Path):
    """Noms des figures produites par un script (ligne « # sorties: a, b »), sinon son nom."""
    for ligne in src.read_text().splitlines()[:5]:
        if ligne.startswith("# sorties:"):
            return [n.strip() for n in ligne.split(":", 1)[1].split(",") if n.strip()]
    return [src.stem]


def construire_py(src: Path) -> str:
    env = dict(os.environ, MPLBACKEND="Agg")
    r = subprocess.run([sys.executable, src.name], cwd=GRAPHIQUES,
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return f"ÉCHEC {src.name}\n{r.stderr[-1500:]}"
    return f"ok   {src.name}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    SORTIE.mkdir(parents=True, exist_ok=True)
    latex = trouver_latex()

    communs_py = [GRAPHIQUES / "style.py"]

    taches = []
    for src in sorted(SCHEMAS.glob("fig-*.tex")):
        if args and src.stem not in args:
            continue
        if force or args or perime(SORTIE / f"{src.stem}.pdf", dependances_tex(src)):
            taches.append(("tex", src))
    for src in sorted(GRAPHIQUES.glob("fig-*.py")):
        if args and src.stem not in args:
            continue
        deps = [src] + communs_py + dependances_donnees(src)
        if force or args or any(perime(SORTIE / f"{n}.pdf", deps) for n in sorties_py(src)):
            taches.append(("py", src))

    if not taches:
        print("Toutes les figures sont à jour.")
        return
    print(f"{len(taches)} figure(s) à construire…")
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        res = ex.map(lambda t: construire_tex(t[1], latex) if t[0] == "tex"
                     else construire_py(t[1]), taches)
        echecs = 0
        for r in res:
            print(r)
            echecs += r.startswith("ÉCHEC")
    if echecs:
        sys.exit(f"{echecs} échec(s)")


if __name__ == "__main__":
    main()
