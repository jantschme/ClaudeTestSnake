# Mammoth Game Overhaul - Implementation Progress

**Date:** 2026-03-12
**Status:** In Progress (Phase 1/3 Complete)

## Summary
Implementing comprehensive UX and visual overhaul for Mammoth snake game. Breaking down into 3 phases.

---

## Phase 1: Core Infrastructure ✅ COMPLETED

### Completed
- [x] **Constants Updated**
  - CELL: 44 → 64 pixels (+45%)
  - COLS: 20 → 16
  - ROWS: 16 → 12
  - W: 880 → 1024, H: 758 → 828
  - FPS: 10 → 8 (slower base speed)
  - RENDER_FPS: 60 (new render target)
  - SPEED_MULT: adjusted (0.55/0.80/1.20)

- [x] **Head Drawing Refactor**
  - `draw_head_mammoth()`, `draw_head_bunny()`, `draw_head_bear()` now take pixel coords (px, py) instead of grid coords
  - Removed internal grid-to-pixel conversion
  - All head drawing functions aligned

- [x] **Transition System**
  - Added `Transition` class with fade-in/fade-out support
  - `begin()`, `update()`, `draw()` methods
  - Smooth black fade between screens (12 alpha per frame)

- [x] **Smooth Movement Infrastructure**
  - Added `prev_snake` tracking for interpolation source
  - Added `move_t` variable (0.0 → 1.0) for interpolation progress
  - `draw_game_scene()` updated to accept interpolation parameters
  - Interpolation math: `lerp(prev, curr, move_t)` for head position

- [x] **Logic-Render Tick Separation**
  - Game logic runs at FPS speed (8 Hz base)
  - Rendering runs at RENDER_FPS (60 Hz)
  - `last_logic_ms` tracking for delta timing
  - `move_t` calculated from elapsed time between logic ticks

- [x] **Menu Integration**
  - Character selection moved into main menu as 3 clickable cards
  - Cards show body, food, character name
  - Selected card highlighted with BTN_SEL color and TUSK_C border
  - Removed separate `char_select` state

- [x] **Font Size Adjustment**
  - font_big: 56 → 64
  - font_med: 30 → 34
  - font_small: 20 → 23

### Code State
- Syntax valid ✓
- Main loop operational
- State machine: menu → mode_select → playing ⇄ paused → dead → menu
- All state transitions use `transition.begin()` for fade effects
- Playing ↔ paused remains instant (no fade)

---

## Phase 2: Polish & Visual Details ⏳ TODO

### Tasks (in order)
1. **Update `draw_mode_select()`**
   - Adjust layout for new screen size (W=1024)
   - Add mode icons (clock for Time Attack, etc.)
   - Optional: card-style layout matching menu

2. **Update `draw_settings()`**
   - Adjust button positions for W=1024, H=828
   - Layout: Language, Speed, Grid, Sound rows with 2-3 buttons each

3. **Improve `draw_bg_grid()`** (Menu background)
   - Add diagonal line pattern
   - Add 8-12 floating particles (slow upward drift)
   - Add 3-stage overlay gradient (dark edges → light center)

4. **Enhance `draw_game_scene()`**
   - Add subtle point-noise pattern (15% alpha) over play area
   - Optional: Checkerboard pattern (±4 brightness on even/odd cells)
   - Add 2px border around play field
   - Optional: Vignette shadow at edges

5. **Improve `draw_btn()`** button styling
   - Add shadow: 3px offset (black, 80 alpha)
   - Add inner border: 2px in MF color on hover
   - Pressed effect: inset by 2px on click

6. **Test Head Rendering**
   - Verify mammoth trunk wobble still works
   - Check that interpolation doesn't break head animation
   - Character switching in menu works smoothly

---

## Phase 3: Testing & Final Polish ⏳ TODO

### Tasks
1. **Full Gameplay Test**
   - Start game from menu
   - Verify smooth movement (no jump artifacts)
   - Test all 4 modes
   - Check pause/resume
   - Verify death screen

2. **Visual Quality Check**
   - Compare character size (CELL=64)
   - Verify screen size matches (1024×828)
   - Speed reduction feels right
   - Transitions are smooth (no stutter)

3. **Build & Package**
   - Test: `python3 snake.py` runs cleanly
   - Test: `python3 -m PyInstaller Mammoth.spec` builds
   - Sign & run macOS app: `codesign` + `open dist/Mammoth.app`

4. **Edge Cases**
   - Very fast ESC mashing doesn't break states
   - Character/mode changes persist in saves
   - Window resize/full-screen (if applicable)

---

## Known Issues / Blockers
- None currently blocking execution

## Notes for Next Session
- The main loop is functional but hasn't been tested live yet
- `draw_mode_select()` and `draw_settings()` may need coordinate adjustments for new screen size
- Interpolation is ready but untested visually—watch for any jitter
- The transition fade system is simple but effective; can enhance with more effects later

## Files Modified
- `snake.py` (~1050 lines) — all changes in single file per architecture
