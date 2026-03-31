# ♟️ Jeu d'Échecs en Python — avec `qtido`

> Projet Python — jeu d'échecs à 2 joueurs avec interface graphique et validation des mouvements.

🚧 **Statut du projet : presque terminé — entièrement jouable et perfectible.**

---

## Table des matières

- [Ce que fait le projet](#ce-que-fait-le-projet)
- [Ce qu'il faut installer](#ce-quil-faut-installer)
- [Comment installer et lancer](#comment-installer-et-lancer)
- [Comment jouer](#comment-jouer)
- [Comment le code fonctionne](#comment-le-code-fonctionne)
- [Limitations connues](#limitations-connues)

---

## Ce que fait le projet

![Capture d'écran de l'échiquier](screenshot.png)

Ce projet est un jeu d'échecs deux joueurs entièrement écrit en Python. Il affiche un vrai échiquier dans une fenêtre graphique et les joueurs saisissent leurs coups dans le terminal.

Ce qui rend ce projet intéressant, c'est que **chaque pièce est dessinée de zéro** à partir de formes basiques — cercles, rectangles et polygones. Il n'y a aucune image, aucun fichier externe, aucun sprite. Le plateau, les pions, la reine, le roi — tout est généré directement par le code.

Le jeu intègre également un **système complet de validation des mouvements** : il vérifie que la pièce appartient au bon joueur, que la destination est bien sur le plateau, qu'on ne capture pas ses propres pièces, et que le mouvement respecte les règles des échecs propres à chaque pièce.

- Les **pièces blanches** sont dessinées en **jaune**
- Les **pièces noires** sont dessinées en **noir**
- Les colonnes vont de **A à H**, les lignes de **1 à 8**

---

## Ce qu'il faut installer

### Python

Il faut Python **3.10 ou supérieur** car le code utilise `match/case`, une fonctionnalité ajoutée à partir de Python 3.10.

### `qtido`

`qtido` est une bibliothèque Python éducative avec des fonctions simples nommées en français, conçue pour apprendre la programmation.

> ⚠️ `qtido` n'est **pas** basé sur la bibliothèque `turtle` de Python. Il est construit par-dessus **PyQt5**, qui est une interface Python pour le framework graphique Qt. C'est Qt qui ouvre la fenêtre et dessine les formes. Le nom « qtido » vient de **Qt** (l'outil graphique utilisé en dessous) et de **ido** (une langue universelle).

### `numpy`

Utilisé pour une seule fonction : `logical_xor`. Elle permet de vérifier qu'une tour se déplace en ligne droite — soit horizontalement soit verticalement, mais jamais les deux à la fois.

---

## Comment installer et lancer

### Étape 1 — Créer un environnement virtuel

Un environnement virtuel garde toutes les bibliothèques du projet dans un seul endroit, séparé du reste de l'ordinateur. C'est la bonne façon de gérer les dépendances.

```bash
# Aller dans le dossier du projet
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

> Une fois activé, `(venv)` apparaît au début de chaque ligne du terminal. Tout ce qu'on installe avec `pip` reste dans cet environnement uniquement.

### Étape 2 — Installer les bibliothèques

```bash
# PyQt5 en premier — qtido en a besoin pour fonctionner
pip install pyqt5

# Puis qtido
pip install qtido

# Puis numpy
pip install numpy
```

> 💡 Sur Linux on peut aussi utiliser :
> ```bash
> sudo apt install python3-pyqt5 python3-numpy
> ```

### Étape 3 — Vérifier que tout est installé

```bash
python3 -c "from qtido import *; print('qtido OK')"
python3 -c "import numpy; print('numpy OK')"
```

### Étape 4 — Lancer le jeu

```bash
python3 echecs_chess.py
```

La fenêtre graphique s'ouvre automatiquement. On joue en tapant dans le terminal.

---

## Comment jouer

### Les codes de cases

Chaque case a une lettre pour la colonne (A à H) et un chiffre pour la ligne (1 à 8) :

```
     A    B    C    D    E    F    G    H
  ┌────┬────┬────┬────┬────┬────┬────┬────┐
8 │ ♜  │ ♞  │ ♝  │ ♛  │ ♚  │ ♝  │ ♞  │ ♜  │  ← Pièces noires
7 │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │ ♟  │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
  │    │    │    │    │    │    │    │    │
2 │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │ ♙  │
1 │ ♖  │ ♘  │ ♗  │ ♔  │ ♕  │ ♗  │ ♘  │ ♖  │  ← Pièces blanches
  └────┴────┴────┴────┴────┴────┴────┴────┘
```

### Déroulement d'un tour

1. Le terminal annonce à quel joueur c'est le tour — **BLANC** ou **NOIR**
2. On tape le code de la case de la pièce à déplacer (exemple : `E2`)
3. On tape le code de la case de destination (exemple : `E4`)
4. Si le coup est invalide, le jeu le signale et demande de réessayer
5. L'échiquier se met à jour dans la fenêtre après chaque coup valide
6. À la fin de chaque tour complet, le jeu demande si on veut continuer

```
C'est au tour du joueur BLANC tes pions sont en ligne 7 :
Quel est le code de la pièce à déplacer ? E7
Quel est le code de la case destinataire ? E5
```

---

## Comment le code fonctionne

### Dessiner le plateau

Le plateau est dessiné en parcourant les 64 cases avec deux boucles imbriquées. Chaque case est colorée en blanc ou gris foncé selon que la somme de ses indices de ligne et colonne est paire ou impaire — c'est ce qui crée le motif de damier.

### Dessiner les pièces

Chaque pièce a sa propre fonction de dessin, construite entièrement à partir de formes basiques :

| Fonction | Pièce | Formes utilisées |
|---|---|---|
| `tracer_pion` | Pion | cercle (tête) + rectangle (corps) |
| `tracer_tour` | Tour | 2 rectangles superposés |
| `tracer_fou` | Fou | cercle + triangle |
| `tracer_chevalier` | Cavalier | polygone à 6 points (forme de tête de cheval) |
| `tracer_reine` | Reine | polygone en couronne à 7 points |
| `tracer_roi` | Roi | rectangle + croix en 3 rectangles |

La fonction `dessiner()` lit le nom de la pièce (ex. `"reine-B"`) et appelle automatiquement la bonne fonction de dessin.

### Comment l'échiquier est stocké en mémoire

L'échiquier est une liste de 8 listes, chacune contenant 8 chaînes de caractères. Chaque chaîne est soit un nom de pièce comme `"pion-B"`, soit une chaîne vide `""` pour une case vide.

```python
[
  ["tour-N", "chevalier-N", "fou-N", "reine-N", "roi-N", ...],  # ligne 8 — arrière des noirs
  ["pion-N", "pion-N", "pion-N", ...],                          # ligne 7 — pions noirs
  ["", "", "", "", "", "", "", ""],                              # lignes vides
  ...
  ["pion-B", "pion-B", "pion-B", ...],                          # ligne 2 — pions blancs
  ["tour-B", "chevalier-B", "fou-B", "roi-B", "reine-B", ...],  # ligne 1 — arrière des blancs
]
```

- `-B` = pièce Blanche
- `-N` = pièce Noire

### Convertir un code de case en position dans le tableau

`de_code_a_num_case("E4")` convertit un code de case en indices `[ligne, colonne]` :
- Ligne : `int("4") - 1 = 3`
- Colonne : `ord("E") - ord("A") = 4`

### Comment les mouvements sont validés

Avant chaque déplacement, `checker_le_move()` effectue ces vérifications dans l'ordre :

1. La case de départ n'est pas vide
2. Le joueur n'essaie pas de capturer sa propre pièce
3. Les codes de cases sont valides et dans le plateau
4. La pièce appartient bien au joueur courant
5. Le mouvement respecte les règles propres à ce type de pièce

Règles de déplacement par pièce :

| Pièce | Règle |
|---|---|
| Tour | Même ligne ou même colonne uniquement (XOR — pas les deux) |
| Fou | Diagonal uniquement — l'écart en colonne doit égaler l'écart en ligne |
| Cavalier | En L — décalages de (2,1) ou (1,2) |
| Roi | 1 case dans n'importe quelle direction |
| Reine | Tour + Fou combinés |
| Pion blanc | Monte (ligne diminue), capture en diagonale, double pas depuis la ligne 6 |
| Pion noir | Descend (ligne augmente), capture en diagonale, double pas depuis la ligne 1 |

---

## Limitations connues

Le jeu est entièrement jouable mais certaines règles des échecs ne sont pas encore implémentées. Ce sont des manques normaux et honnêtes pour une première version de ce type de projet.

**✅ Ce qui fonctionne déjà**
- Les 6 types de pièces se déplacent selon leurs règles
- La capture des pièces adverses
- Le double pas initial des pions depuis la ligne de départ
- L'alternance correcte des tours
- Le rafraîchissement visuel du plateau après chaque coup
- Les coups invalides sont refusés avec un message d'erreur
- La partie continue jusqu'à ce que les joueurs décident d'arrêter

**❌ Ce qui n'est pas encore implémenté**

- **Détection de l'échec et de l'échec et mat** — le jeu ne détecte pas quand un roi est en échec. Un joueur peut ignorer un échec et continuer à jouer librement, ce qui n'est pas permis aux échecs.

- **Vérification des pièces sur le chemin** — les tours, fous et reines peuvent actuellement traverser d'autres pièces. Aux vrais échecs, une pièce ne peut pas sauter par-dessus une autre (sauf le cavalier). Corriger cela nécessiterait de vérifier toutes les cases entre le départ et la destination.

- **Le roque** — le mouvement spécial où le roi et une tour échangent leurs positions n'est pas implémenté.

- **La prise en passant** — la règle spéciale de capture du pion qui s'applique juste après le double pas de l'adversaire n'est pas implémentée.

- **La promotion du pion** — quand un pion atteint la dernière ligne, il devrait devenir une reine (ou une autre pièce). Pour l'instant il reste un pion.

- **Gestion des erreurs de saisie** — si un joueur tape quelque chose d'invalide comme `"Z9"` ou appuie simplement sur Entrée, le programme plantera. Ajouter une vérification simple du format de l'entrée suffirait à corriger ça.

- **Condition de fin de partie** — le jeu s'arrête uniquement quand un joueur tape `non`. Il n'y a pas de fin automatique quand un roi est capturé.

---

## Désactiver le venv quand on a fini

```bash
deactivate
```
