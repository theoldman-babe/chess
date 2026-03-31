# chess
# ♟️ Chess Game in Python — with `qtido`

A two-player chess game combining a graphical window and terminal input, built in Python using the `qtido` library for rendering and `numpy` for move validation logic.

> 🚧 **Project status: nearly complete — functional but open for improvement.** The core game loop, all piece movements, and the graphical rendering are fully working (see screenshot below). Several chess rules are still missing and are listed in the [Known Limitations](#known-limitations) section.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [How to Play](#how-to-play)
- [Code Structure](#code-structure)
- [Known Limitations](#known-limitations)

---

## Project Overview

![Chess board screenshot](screenshot.png)

The program displays an 8×8 chessboard in a 900×900 pixel graphical window. Every piece is drawn manually using basic shapes (rectangles, discs, and polygons). Both players take turns entering square codes in the terminal (e.g. `E2` → `E4`).

- **White pieces** (B) are drawn in **yellow**
- **Black pieces** (N) are drawn in **black**
- Columns are labelled **A to H**, rows **1 to 8**

---

## Dependencies

### `qtido`

`qtido` is an educational Python library designed to make learning programming simple and accessible, with clearly named functions written in **French**.

> ⚠️ **Important:** `qtido` is **not** a wrapper around Python's `turtle` library. It is a wrapper around **PyQt5** (Qt for Python). It relies on the Qt framework to create graphical windows and draw shapes. It does have an optional turtle-like mode (`creer_tortue`), but that is not its core mechanism. The name "qtido" is actually a blend of **Qt** (the graphics framework it is built on) and **ido** (a universal language).

`qtido` functions used in this project:

| Function | Role |
|---|---|
| `creer(w, h)` | Creates a graphical window of size w×h |
| `couleur(f, r, g, b)` | Sets the current drawing colour (values from 0 to 1) |
| `rectangle(f, x1, y1, x2, y2)` | Draws a filled rectangle |
| `disque(f, x, y, r)` | Draws a filled disc of radius r |
| `polygone(f, points)` | Draws a polygon from a list of points |
| `texte(f, x, y, size, s)` | Renders text on the window |
| `re_afficher(f)` | Refreshes / repaints the window |
| `attendre_fermeture(f)` | Blocks execution until the window is closed |

### `numpy`

Used solely for the `logical_xor` function, which validates **rook moves** — a rook can move along a row or a column, but not both at the same time. `logical_xor` expresses this constraint in a single, clean line.

### Python version

Python **3.8 or higher** is required. Python **3.10+** is recommended since the code uses `match/case` syntax (structural pattern matching).

---

## Installation

### 1. Create a virtual environment (strongly recommended)

Using a **venv** isolates this project's dependencies from the rest of your Python installation, preventing version conflicts.

```bash
# Navigate to your project folder
cd path/to/your/project

# Create the virtual environment
python3 -m venv venv

# Activate it
# On Linux / macOS:
source venv/bin/activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (cmd):
venv\Scripts\activate.bat
```

> Once activated, your terminal prompt shows `(venv)` at the start of each line. All `pip install` commands below will install packages inside this venv only, not system-wide.

### 2. Install the dependencies

```bash
# PyQt5 must be installed first — qtido is built on top of it
pip install pyqt5

# Install qtido
pip install qtido

# Install numpy
pip install numpy
```

> 💡 On some Linux systems, you can also install PyQt5 and numpy via the system package manager:
> ```bash
> sudo apt install python3-pyqt5 python3-numpy
> ```

### 3. Verify the installation

```bash
python3 -c "from qtido import *; print('qtido OK')"
python3 -c "import numpy; print('numpy OK')"
```

---

## Running the Game

With the venv activated, navigate to the folder containing the chess file and run:

```bash
python3 echecs_chess.py
```

A 900×900 graphical window will open showing the board. All player interaction happens **in the terminal**.

---

## How to Play

### Square notation

Squares are identified by a **letter** (column, A to H) followed by a **number** (row, 1 to 8):

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

### Turn flow

1. The terminal announces whose turn it is (**WHITE** or **BLACK**)
2. Enter the **code of the piece you want to move** (e.g. `E2`)
3. Enter the **code of the destination square** (e.g. `E4`)
4. If the move is invalid, an error message is shown and you can try again
5. The board updates visually in the graphical window
6. After each full round, the game asks whether you want to keep playing

```
C'est au tour du joueur BLANC tes pions sont en ligne 7 :
Quel est le code de la pièce à déplacer ? E7
Quel est le code de la case destinataire ? E5
```

### Starting position

```
Row 8 (Black) : Rook - Knight - Bishop - Queen - King - Bishop - Knight - Rook
Row 7 (Black) : Pawn × 8
...
Row 2 (White) : Pawn × 8
Row 1 (White) : Rook - Knight - Bishop - King - Queen - Bishop - Knight - Rook
```

> 💡 Note: the **White King and Queen positions are swapped** compared to standard chess convention (King on D1, Queen on E1 in this code instead of the usual King on E1, Queen on D1).

---

## Code Structure

### Board rendering

```
tracer_plateau()
  └── dessiner_cases_vides(row, col)      # colours each square (checkerboard)
        └── tracer_rectangle_couleur()   # white or dark grey based on parity
```

### Piece drawing

Each piece is built from basic geometric primitives:

| Function | Piece | Shapes used |
|---|---|---|
| `tracer_pion` | Pawn | disc (head) + rectangle (body) |
| `tracer_tour` | Rook | 2 stacked rectangles |
| `tracer_fou` | Bishop | disc + triangle (polygon) |
| `tracer_chevalier` | Knight | irregular polygon (horse head) |
| `tracer_reine` | Queen | crown-shaped polygon |
| `tracer_roi` | King | rectangle + cross (3 rectangles) |

The `dessiner(f, s, x, y)` function acts as a dispatcher: it reads the piece name (e.g. `"reine-B"`) and calls the correct drawing function.

### Board representation

The board is a **list of 8 lists** (8×8 matrix) of strings:

```python
[
  ["tour-N", "chevalier-N", ..., "tour-N"],  # index 0 = row 8 on screen
  ["pion-N",  "pion-N",  ..., "pion-N" ],
  ["", "", "", "", "", "", "", ""],           # empty rows
  ...
  ["pion-B",  "pion-B",  ..., "pion-B" ],
  ["tour-B", "chevalier-B", ..., "tour-B"],  # index 7 = row 1 on screen
]
```

- Suffix `-N` = **Black** piece (*Noir*)
- Suffix `-B` = **White** piece (*Blanc*)
- Empty square = empty string `""`

### Coordinate conversion

`de_code_a_num_case("E4")` → `[3, 4]` (row index 3, column index 4 in the matrix)

- Row: `int("4") - 1 = 3`
- Column: `ord("E") - ord("A") = 4`

### Move validation

`checker_le_move(board, from_square, to_square, player)` returns `True` or `False`.

Checks performed in order:
1. The source square is not empty
2. You are not capturing your own piece
3. Both coordinates are within the board (0–7)
4. The piece belongs to the current player
5. The move follows the piece-specific movement rules (via `match/case`)

Rules per piece:

| Piece | Rule implemented |
|---|---|
| Rook | Straight line only (XOR: same column or same row, not both) |
| Bishop | Diagonal only (`Δcol == Δrow`) |
| Knight | L-shape: (2,1) or (1,2) offset |
| King | 1 square in any direction |
| Queen | Rook + Bishop combined |
| White Pawn | Moves toward decreasing rows, diagonal capture, double step from row 6 |
| Black Pawn | Moves toward increasing rows, diagonal capture, double step from row 1 |

---

## Known Limitations

The project is nearly complete and fully playable, but the following features are missing or imperfect — great candidates for future improvements:

**✅ Already working**
- Basic movement for all 6 piece types
- Capturing opponent pieces
- Pawn double-step from the starting row
- Turn alternation between White and Black
- Graphical board refresh after every move
- Input validation with error feedback

**❌ Not yet implemented**
- **Check / checkmate detection** — the game does not end when the king is in check
- **Castling** — the special king + rook move is not supported
- **En passant** — the special pawn capture is not supported
- **Pawn promotion** — a pawn reaching the last row stays a pawn
- **Path obstruction** — rooks, bishops and queens can currently jump over pieces (the path between source and destination is not checked)
- **Game-over condition** — the game only stops if the player manually types `non` when prompted

---

## Deactivating the venv

Once you are done playing or working on the project:

```bash
deactivate
```
