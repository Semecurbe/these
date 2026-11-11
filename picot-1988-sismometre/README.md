# Picot (1988) — Étude d'un sismomètre : transcription Quarto

Transcription de la thèse de Docteur Ingénieur de Jean-Daniel Picot (1988).
Le texte est dans `chapitres/` et le document maître est `picot-1988-sismometre.qmd`.

## Figures

Les figures sont produites **hors de Quarto**. Le rendu du document ne fait
qu'inclure des fichiers déjà générés, ce qui garde la compilation rapide.

| Dossier | Contenu |
|---|---|
| `schemas/` | Schémas TikZ (`fig-*.tex`, classe `standalone`). Préambule commun : `_preambule.tex` ; fragments partagés : `_*.tex` |
| `graphiques/` | Graphiques matplotlib (`fig-*.py`). Style commun (polices Latin Modern, palette, aides) : `style.py` |
| `graphiques/donnees/` | Données des courbes (CSV), numérisées à partir de l'original |
| `graphiques/numerisation/` | Scripts de numérisation des scans (spectres, enregistrements, lame) |
| `figures/generees/` | Sorties : `.pdf` (inclus par LaTeX) et `.svg` (inclus par le HTML) |
| `figures/scans/` | Figures scannées d'origine, conservées pour comparaison |

### Construire les figures

```sh
python3 construire_figures.py              # ne reconstruit que ce qui a changé
python3 construire_figures.py fig-2-2-3    # une ou plusieurs figures
python3 construire_figures.py --force      # tout reconstruire
```

Les dépendances sont gérées. Un schéma est reconstruit si son fichier `.tex`,
le préambule ou un fragment qu'il inclut a changé. Un graphique est reconstruit
si son script, `style.py` ou les données qu'il lit ont changé.

Pour qu'un script produise plusieurs figures, il les déclare sur l'une de ses
premières lignes, par exemple `# sorties: fig-5-1-2, fig-5-1-3`.

Prérequis : `pdflatex` avec `circuitikz` (TinyTeX convient :
`tlmgr install circuitikz`), `pdftocairo` (poppler), Python 3 avec `matplotlib`
et `numpy`.

### Compiler le document

Le document est un **livre Quarto** : le projet est défini par `_quarto.yml`,
avec un fichier par chapitre dans `chapitres/` et les pages liminaires dans
`index.qmd`.

```sh
quarto render                 # HTML (site paginé par chapitre) et PDF
quarto render --to pdf        # PDF seul : _book/picot-1988-sismometre.pdf
quarto render --to html       # HTML seul : _book/index.html
quarto preview                # aperçu HTML avec rechargement automatique
```

Les images sont référencées sans extension (`../figures/generees/fig-2-0-1`).
Le format HTML choisit le `.svg` et le format PDF le `.pdf`, grâce à
`default-image-extension`.

Mise en forme :

- **PDF** : classe KOMA `scrbook`. La page de titre est dans
  `tex/before-body.tex` et lit le bloc `these:` de `_quarto.yml`. Les réglages
  de typographie, en-têtes et légendes sont dans `tex/preambule.tex`. Les
  pages liminaires sont en chiffres romains et suivies de la table des
  matières et de la liste des figures.
- **HTML** : thème `cosmo` personnalisé par `style/these.scss`. Les figures
  s'agrandissent au clic, les notes s'affichent en marge, et une recherche
  plein texte est disponible.
- **Bibliographie** : `references.bib`, citée dans le texte (`@melton1976`).
- **Numérotation** : seuls les chapitres sont numérotés par Quarto. Les
  numéros de paragraphes (2.1, 2.1.2…), de figures et de tableaux sont ceux
  de l'original et figurent dans les titres et les légendes. Chaque figure
  porte une légende courte (`fig-scap`) pour la liste des figures.

### Origine des données des graphiques

- **Courbes calculées** à partir des formules et des paramètres du texte :
  réponses des oscillateurs, gain de boucle et lieu de Nyquist, courbes iso
  dM/dφ, constante de couple des pivots, admittances.
- **Spectres mesurés**, numérisés automatiquement à partir des scans
  (`numerisation/numeriser_spectres.py`) : chaque page est rendue à 300 dpi,
  les axes sont calibrés sur le quadrillage, puis le quadrillage et les textes
  sont masqués.
- **Enregistrements papier** (Fig. 4.2.1, 4.2.5, 4.2.6), numérisés par suivi
  de tracé (`numerisation/numeriser_enregistrements.py`). Les échelles
  physiques viennent des légendes de l'original.
- **Courbes tracées à la main** (spectres de bruit de référence, asymptotes
  de bruit et de dynamique), relevées point par point sur une grille calibrée
  superposée au scan. Ces relevés sont dans les CSV correspondants.

Le script `numerisation/superposer.py` superpose les données numérisées aux
scans pour les contrôler.
