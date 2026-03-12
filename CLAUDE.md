# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Mammoth" – a Snake game in Python/Pygame. Three playable characters (Mammoth, Bunny, Bear), each with a unique food item and head art. Four game modes (Classic, Time Attack, Zen, Obstacles). Particle effects, procedural sound, pause support, and persistent save (settings + per-character/mode high scores).

## Running & Building

**Run directly:**
```bash
python3 snake.py
```

**Build macOS app bundle:**
```bash
rm -rf dist build && python3 -m PyInstaller Mammoth.spec
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

All game code lives in a single file: `snake.py` (~960 lines).

**File structure:**

| Lines | Section |
|-------|---------|
| 1–115 | Config, colors, CHARACTERS/CHAR_FOOD dicts, translations (DE/EN) |
| 116–150 | Persistence: `load_save()`, `write_save()` → `~/Library/Application Support/Mammoth/save.json` |
| 151–185 | Sound: `init_sounds()`, `play_snd()` – procedural tones via `array` module |
| 186–220 | Drawing primitives: `fcirc()`, `fur_strokes()` |
| 221–300 | Animal heads: `draw_head_mammoth()`, `draw_head_bunny()`, `draw_head_bear()`, dispatcher `draw_head()` |
| 301–380 | Food surfaces: `make_lolly_surf()`, `make_carrot_surf()`, `make_honeypot_surf()`, `make_food_surf()` |
| 381–420 | Particles: `Particle`, `emit_particles()`, `update_particles()`, `draw_particles()` |
| 421–470 | UI helpers: `draw_grid()`, `draw_centered()`, `dark_overlay()`, `make_rect()`, `draw_btn()`, `was_clicked()` |
| 471–510 | Game logic: `random_food()`, `random_obstacles()`, `new_game()`, `get_speed()` |
| 511–530 | HUD: `draw_hud()`, `draw_game_scene()` |
| 531–700 | Screen renderers: `draw_menu()`, `draw_char_select()`, `draw_mode_select()`, `draw_settings()` |
| 701–961 | Main loop: state machine, events, rendering |

**State machine:**
```
menu → char_select → mode_select → playing ⇄ paused
                                          ↓
                                        dead → menu (ESC) / playing (SPACE)
menu → settings → menu
```

**Persistence:** `save` dict holds `high_scores` (keyed `"{character}_{mode}"`), `language`, `speed`, `show_grid`, `sound`, `last_character`, `last_mode`. Written on settings-back, ESC-to-menu, quit, and new high score.

**Game modes:** `classic` (standard), `timeattack` (60s countdown), `zen` (wrap walls), `obstacles` (random blocks).

**Characters:** `mammoth` (lolly), `bunny` (carrot), `bear` (honey).

**Controls:**
- Arrow keys / WASD to move
- P or ESC (while playing) → pause; P resumes, ESC → menu
- SPACE/ENTER to restart after death
- Mouse clicks on all buttons

**App Store prep:** `Mammoth.spec` sets `bundle_identifier='com.mammoth.game'`, `version='1.0.0'`, `LSMinimumSystemVersion='11.0'`, `NSHighResolutionCapable`. `Mammoth.entitlements` enables App Sandbox + file access.

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

## Token Optimization

**Clear chat after each task** to avoid token bloat in long conversations.

Workflow:
1. Complete one focused task (e.g., implement `draw_mode_select()`)
2. Commit and push to GitHub
3. Clear/end the chat session
4. Start fresh session for next task
5. Pick next task from `TaskList`

This keeps individual conversations under 50K tokens and saves significant token spend on the 9-task overhaul.
