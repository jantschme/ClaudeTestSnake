# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Mammoth" – a Snake game clone in Python/Pygame where the player controls a mammoth collecting pink lollipops.

## Running & Building

**Run directly:**
```bash
python3 snake.py
```

**Build macOS app bundle:**
```bash
rm -rf dist build && python3 -m PyInstaller --windowed --onedir --name "Mammoth" snake.py
```

**Sign and run the app (macOS):**
```bash
xattr -cr dist/Mammoth.app && codesign --force --deep -s - dist/Mammoth.app
open dist/Mammoth.app
```

**Install dependency:**
```bash
pip3 install pygame
```

## Architecture

All game code lives in a single file: `snake.py` (311 lines).

**Structure within `snake.py`:**

| Lines | Section |
|-------|---------|
| 7–37 | Constants: grid (20×16 cells, 44px each), display size (880×854), FPS, direction vectors, color palette |
| 40–162 | Drawing helpers: `fcirc()` (anti-aliased circles), `fur_strokes()` (seeded procedural fur), `make_body_surf()`, `make_lollipop_surf()`, `draw_head()` |
| 186–204 | Game logic: `random_food()`, `new_game()`, `get_speed()` (dynamic FPS scaling with score) |
| 208–307 | Main loop: event handling, state machine (`"start"` → `"playing"` → `"dead"`), collision detection, rendering pipeline, high-score persistence |

**Rendering pipeline per frame:** background → grid → body segments → head → food → HUD → state overlays.

The mammoth head (`draw_head()`) is procedurally rendered each frame with directional tusks and an animated trunk wobble. Body segments are pre-rendered onto a surface (`make_body_surf()`).

**Controls:** Arrow keys / WASD to move, SPACE/ENTER to start, ESC to quit. UI text is in German ("AUSGESTORBEN" = game over).

## Git Workflow

After completing any meaningful unit of work (feature, fix, refactor), commit and push to GitHub:

```bash
git add <specific files>
git commit -m "short descriptive message"
git push
```

**Rules:**
- Commit after every meaningful change — never let work pile up uncommitted.
- Use clear, specific commit messages (e.g. `"add trunk wobble animation"`, `"fix collision detection off-by-one"`).
- Never use `git add -A` or `git add .` — always stage specific files to avoid committing build artifacts or secrets.
- Push to GitHub after every commit so work is never only local.
