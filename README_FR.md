# ♟️ Jeu d'Échecs en Python — avec `qtido`

Un jeu d'échecs deux joueurs combinant une fenêtre graphique et des entrées en terminal, développé en Python avec la bibliothèque `qtido` pour l'affichage et `numpy` pour la logique de validation des mouvements.

> 🚧 **Statut du projet : presque terminé — fonctionnel mais perfectible.** La boucle de jeu principale, les mouvements de toutes les pièces et le rendu graphique fonctionnent entièrement (voir capture d'écran ci-dessous). Plusieurs règles des échecs sont encore manquantes et sont listées dans la section [Limitations connues](#limitations-connues).

---

## 📋 Table des matières

- [Aperçu du projet](#aperçu-du-projet)
- [Dépendances](#dépendances)
- [Installation](#installation)
- [Lancer le jeu](#lancer-le-jeu)
- [Comment jouer](#comment-jouer)
- [Structure du code](#structure-du-code)
- [Limitations connues](#limitations-connues)

---

## Aperçu du projet

![Capture d'écran de l'échiquier](screenshot.png)

Le programme affiche un échiquier 8×8 dans une fenêtre graphique de 900×900 pixels. Chaque pièce est dessinée manuellement à l'aide de formes basiques (rectangles, disques et polygones). Les deux joueurs jouent à tour de rôle en saisissant des codes de cases dans le terminal (ex. `E2` → `E4`).

- Les **pièces blanches** (B) sont dessinées en **jaune**
- Les **pièces noires** (N) sont dessinées en **noir**
- Les colonnes sont étiquetées **A à H**, les lignes **1 à 8**

---

## Dépendances

### `qtido`

`qtido` est une bibliothèque Python éducative conçue pour rendre l'apprentissage de la programmation simple et accessible, avec des fonctions aux noms clairs écrits en **français**.

> ⚠️ **Important :** `qtido` n'est **pas** une surcouche de la bibliothèque `turtle` de Python. C'est une surcouche de **PyQt5** (Qt pour Python). Elle s'appuie sur le framework Qt pour créer des fenêtres graphiques et dessiner des formes. Elle possède bien un mode tortue optionnel (`creer_tortue`), mais ce n'est pas son fonctionnement principal. Le nom « qtido » est d'ailleurs un mélange de **Qt** (le framework graphique sur lequel elle est construite) et de **ido** (langue universelle).

Fonctions `qtido` utilisées dans ce projet :

| Fonction | Rôle |
|---|---|
| `creer(w, h)` | Crée une fenêtre graphique de taille w×h |
| `couleur(f, r, g, b)` | Définit la couleur courante (valeurs entre 0 et 1) |
| `rectangle(f, x1, y1, x2, y2)` | Dessine un rectangle plein |
| `disque(f, x, y, r)` | Dessine un disque plein de rayon r |
| `polygone(f, points)` | Dessine un polygone à partir d'une liste de points |
| `texte(f, x, y, taille, s)` | Affiche du texte sur la fenêtre |
| `re_afficher(f)` | Rafraîchit / repeint la fenêtre |
| `attendre_fermeture(f)` | Bloque l'exécution jusqu'à la fermeture de la fenêtre |

### `numpy`

Utilisé uniquement pour la fonction `logical_xor`, qui valide les **déplacements de la tour** — une tour peut se déplacer en ligne ou en colonne, mais pas les deux à la fois. `logical_xor` exprime cette contrainte en une seule ligne claire.

### Version Python

Python **3.8 ou supérieur** est requis. Python **3.10+** est recommandé car le code utilise la syntaxe `match/case` (filtrage par motif structurel).

---

## Installation

### 1. Créer un environnement virtuel (fortement recommandé)

L'utilisation d'un **venv** isole les dépendances de ce projet du reste de ton installation Python, évitant ainsi les conflits de versions.

```bash
# Se placer dans le dossier du projet
cd chemin/vers/ton/projet

# Créer le venv
python3 -m venv venv

# L'activer
# Sur Linux / macOS :
source venv/bin/activate

# Sur Windows (PowerShell) :
venv\Scripts\Activate.ps1

# Sur Windows (cmd) :
venv\Scripts\activate.bat
```

> Une fois activé, le terminal affiche `(venv)` au début de chaque ligne. Toutes les commandes `pip install` ci-dessous installeront les paquets dans ce venv uniquement, pas sur le système.

### 2. Installer les dépendances

```bash
# PyQt5 doit être installé en premier — qtido est construit par-dessus
pip install pyqt5

# Installer qtido
pip install qtido

# Installer numpy
pip install numpy
```

> 💡 Sur certains systèmes Linux, PyQt5 et numpy peuvent aussi être installés via le gestionnaire de paquets système :
> ```bash
> sudo apt install python3-pyqt5 python3-numpy
> ```

### 3. Vérifier l'installation

```bash
python3 -c "from qtido import *; print('qtido OK')"
python3 -c "import numpy; print('numpy OK')"
```

---

## Lancer le jeu

Avec le venv activé, place-toi dans le dossier contenant le fichier du jeu et lance :

```bash
python3 echecs_chess.py
```

Une fenêtre graphique de 900×900 pixels s'ouvre avec l'échiquier. Toutes les interactions se font **dans le terminal**.

---

## Comment jouer

### Notation des cases

Les cases sont désignées par une **lettre** (colonne, A à H) suivie d'un **chiffre** (ligne, 1 à 8) :

```
     A    B    C    D    E    F    G    H
  ┌────┬────┬────┬────┬────┬────┬────┬────┐
8 │ ♜  │ ♞  │ ♝  │ ♛  │ ♚  │ ♝  │ ♞  │ ♜  │
7 │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
2 │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │
1 │ ♖  │ ♘  │ ♗  │ ♔  │ ♕  │ ♗  │ ♘  │ ♖  │
  └────┴────┴────┴────┴────┴────┴────┴────┘
```

### Déroulement d'un tour

1. Le terminal annonce à quel joueur c'est le tour (**BLANC** ou **NOIR**)
2. Saisir le **code de la pièce à déplacer** (ex. `E2`)
3. Saisir le **code de la case de destination** (ex. `E4`)
4. Si le coup est invalide, un message d'erreur s'affiche et on peut réessayer
5. L'échiquier se met à jour visuellement dans la fenêtre graphique
6. Après chaque tour complet, le jeu demande si l'on veut continuer

```
C'est au tour du joueur BLANC tes pions sont en ligne 7 :
Quel est le code de la pièce à déplacer ? E7
Quel est le code de la case destinataire ? E5
```

### Position initiale

```
Ligne 8 (Noirs) : Tour - Cavalier - Fou - Reine - Roi - Fou - Cavalier - Tour
Ligne 7 (Noirs) : Pion × 8
...
Ligne 2 (Blancs) : Pion × 8
Ligne 1 (Blancs) : Tour - Cavalier - Fou - Roi - Reine - Fou - Cavalier - Tour
```

> 💡 Attention : la **position du Roi et de la Reine blancs est inversée** par rapport à la convention standard des échecs (Roi en D1, Reine en E1 dans ce code, au lieu du Roi en E1 et la Reine en D1 habituellement).

---

## Structure du code

### Rendu du plateau

```
tracer_plateau()
  └── dessiner_cases_vides(ligne, colonne)   # colorie chaque case (damier)
        └── tracer_rectangle_couleur()       # blanc ou gris foncé selon la parité
```

### Dessin des pièces

Chaque pièce est construite à partir de primitives géométriques basiques :

| Fonction | Pièce | Formes utilisées |
|---|---|---|
| `tracer_pion` | Pion | disque (tête) + rectangle (corps) |
| `tracer_tour` | Tour | 2 rectangles superposés |
| `tracer_fou` | Fou | disque + triangle (polygone) |
| `tracer_chevalier` | Cavalier | polygone irrégulier (tête de cheval) |
| `tracer_reine` | Reine | polygone en forme de couronne |
| `tracer_roi` | Roi | rectangle + croix (3 rectangles) |

La fonction `dessiner(f, s, x, y)` fait office de dispatcher : elle lit le nom de la pièce (ex. `"reine-B"`) et appelle la bonne fonction de tracé.

### Représentation de l'échiquier

L'échiquier est une **liste de 8 listes** (matrice 8×8) de chaînes de caractères :

```python
[
  ["tour-N", "chevalier-N", ..., "tour-N"],  # index 0 = ligne 8 à l'écran
  ["pion-N",  "pion-N",  ..., "pion-N" ],
  ["", "", "", "", "", "", "", ""],           # lignes vides
  ...
  ["pion-B",  "pion-B",  ..., "pion-B" ],
  ["tour-B", "chevalier-B", ..., "tour-B"],  # index 7 = ligne 1 à l'écran
]
```

- Suffixe `-N` = pièce **Noire**
- Suffixe `-B` = pièce **Blanche**
- Case vide = chaîne vide `""`

### Conversion des coordonnées

`de_code_a_num_case("E4")` → `[3, 4]` (index de ligne 3, index de colonne 4 dans la matrice)

- Ligne : `int("4") - 1 = 3`
- Colonne : `ord("E") - ord("A") = 4`

### Validation des mouvements

`checker_le_move(echiquier, case_départ, case_arrivée, joueur)` retourne `True` ou `False`.

Vérifications effectuées dans l'ordre :
1. La case de départ n'est pas vide
2. On ne capture pas sa propre pièce
3. Les deux coordonnées sont dans le plateau (0–7)
4. La pièce appartient bien au joueur courant
5. Le mouvement respecte les règles propres à la pièce (via `match/case`)

Règles par pièce :

| Pièce | Règle implémentée |
|---|---|
| Tour | Ligne droite uniquement (XOR : même colonne ou même ligne, pas les deux) |
| Fou | Diagonal uniquement (`Δcol == Δligne`) |
| Cavalier | Déplacement en L : décalage (2,1) ou (1,2) |
| Roi | 1 case dans n'importe quelle direction |
| Reine | Combinaison Tour + Fou |
| Pion blanc | Avance vers les lignes décroissantes, capture en diagonale, double pas depuis la ligne 6 |
| Pion noir | Avance vers les lignes croissantes, capture en diagonale, double pas depuis la ligne 1 |

---

## Limitations connues

Le projet est presque terminé et entièrement jouable, mais les fonctionnalités suivantes sont manquantes ou imparfaites — de bons candidats pour de futures améliorations :

**✅ Déjà fonctionnel**
- Déplacement de base pour les 6 types de pièces
- Capture des pièces adverses
- Double pas initial du pion depuis la ligne de départ
- Alternance des tours entre Blanc et Noir
- Rafraîchissement graphique de l'échiquier après chaque coup
- Validation des entrées avec retour d'erreur

**❌ Pas encore implémenté**
- **Détection de l'échec / échec et mat** — le jeu ne s'arrête pas quand le roi est en échec
- **Roque** — le mouvement spécial roi + tour n'est pas supporté
- **Prise en passant** — la capture spéciale du pion n'est pas supportée
- **Promotion du pion** — un pion atteignant la dernière ligne reste un pion
- **Vérification du chemin** — la tour, le fou et la reine peuvent actuellement sauter par-dessus des pièces (le chemin entre la case de départ et d'arrivée n'est pas vérifié)
- **Condition de fin de partie** — le jeu s'arrête uniquement si le joueur tape `non` quand il y est invité

---

## Désactiver le venv

Une fois que tu as fini de jouer ou de travailler sur le projet :

```bash
deactivate
```
