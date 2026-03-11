import pygame
import pygame.gfxdraw
import random
import sys
import math

# ── Config ────────────────────────────────────────────────────────────────────
CELL  = 44
COLS  = 20
ROWS  = 16
W     = COLS * CELL          # 880
GH    = ROWS * CELL          # 704
H     = GH + 54              # 758
FPS   = 10

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = ( 20,  36,  20)
GRID_C   = ( 30,  48,  30)
MB       = (112,  74,  36)
MD       = ( 78,  50,  20)
MF       = (162, 118,  64)
TUSK_C   = (252, 246, 200)
SKIN_C   = ( 92,  58,  24)
EYE_W    = (242, 230, 210)
EYE_P    = ( 15,  10,   4)
PINK     = (255,  88, 165)
PINK_H   = (255, 205, 232)
PINK_D   = (200,  40, 120)
STICK_C  = (200, 168, 128)
TEXT_C   = (228, 232, 220)
HUD_C    = ( 12,  22,  12)
BTN_BG   = ( 35,  60,  35)
BTN_HOV  = ( 55,  90,  55)
BTN_SEL  = ( 45, 105,  38)

RIGHT = ( 1,  0)
LEFT  = (-1,  0)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

SPEED_MULT = {"slow": 0.6, "normal": 1.0, "fast": 1.6}

# ── Translations ──────────────────────────────────────────────────────────────
T = {
    "de": {
        "play":           "SPIELEN",
        "settings_btn":   "EINSTELLUNGEN",
        "quit":           "BEENDEN",
        "language_label": "Sprache",
        "speed_label":    "Geschwindigkeit",
        "grid_label":     "Raster",
        "back":           "ZURÜCK",
        "slow":           "LANGSAM",
        "normal":         "NORMAL",
        "fast":           "SCHNELL",
        "on":             "AN",
        "off":            "AUS",
        "game_over":      "AUSGESTORBEN",
        "score_msg":      "Lollies gegessen: {}",
        "restart_hint":   "Leertaste für neues Spiel",
        "lollies":        "Lollies",
        "record":         "Rekord",
    },
    "en": {
        "play":           "PLAY",
        "settings_btn":   "SETTINGS",
        "quit":           "QUIT",
        "language_label": "Language",
        "speed_label":    "Speed",
        "grid_label":     "Grid",
        "back":           "BACK",
        "slow":           "SLOW",
        "normal":         "NORMAL",
        "fast":           "FAST",
        "on":             "ON",
        "off":            "OFF",
        "game_over":      "EXTINCT",
        "score_msg":      "Lollies eaten: {}",
        "restart_hint":   "Space for new game",
        "lollies":        "Lollies",
        "record":         "Record",
    },
}


# ── Drawing helpers ───────────────────────────────────────────────────────────

def fcirc(surf, color, cx, cy, r):
    """Anti-aliased filled circle."""
    cx, cy, r = int(cx), int(cy), int(r)
    if r <= 0:
        return
    pygame.gfxdraw.filled_circle(surf, cx, cy, r, color)
    pygame.gfxdraw.aacircle(surf, cx, cy, r, color)


def fur_strokes(surf, ox, oy, seed, count=16):
    rng = random.Random(seed)
    c = CELL
    for _ in range(count):
        fx = rng.randint(ox + 4, ox + c - 7)
        fy = rng.randint(oy + 4, oy + c - 7)
        a  = rng.uniform(-1.4, 1.4)
        ln = rng.randint(5, 11)
        ex = max(ox + 2, min(ox + c - 3, fx + int(math.cos(a) * ln)))
        ey = max(oy + 2, min(oy + c - 3, fy + int(math.sin(a) * ln)))
        pygame.draw.line(surf, MF, (fx, fy), (ex, ey), 2)


# ── Precomputed surfaces ──────────────────────────────────────────────────────

def make_body_surf():
    c = CELL
    s = pygame.Surface((c, c), pygame.SRCALPHA)
    r = c // 4
    pygame.draw.rect(s, MB, (2, 2, c - 4, c - 4), border_radius=r)
    pygame.draw.rect(s, MD, (c // 3, c // 3, c * 2 // 3 - 4, c * 2 // 3 - 4), border_radius=r // 2)
    fur_strokes(s, 0, 0, seed=42)
    return s


def make_lollipop_surf():
    c  = CELL
    s  = pygame.Surface((c, c), pygame.SRCALPHA)
    cr = c // 3
    cx = c // 2
    cy = c // 3
    pygame.draw.line(s, STICK_C, (cx, cy + cr - 1), (cx, c - 3), 4)
    pygame.draw.line(s, (230, 200, 158), (cx - 1, cy + cr - 1), (cx - 1, c - 3), 1)
    fcirc(s, PINK_D, cx + 3, cy + 3, cr)
    fcirc(s, PINK, cx, cy, cr)
    pygame.draw.arc(s, (255, 255, 255),
                    (cx - cr + 5, cy - cr + 5, (cr - 5) * 2, (cr - 5) * 2),
                    math.pi * 0.3, math.pi * 1.25, 3)
    pygame.draw.arc(s, (255, 255, 255),
                    (cx - cr // 2 + 3, cy - cr // 2 + 3, (cr // 2 - 3) * 2, (cr // 2 - 3) * 2),
                    math.pi * 1.1, math.pi * 2.1, 2)
    fcirc(s, PINK_H, cx - cr // 3, cy - cr // 3, cr // 3)
    return s


# ── Mammoth head ──────────────────────────────────────────────────────────────

def draw_head(screen, gx, gy, direction):
    c  = CELL
    px = gx * c
    py = gy * c
    cx = px + c // 2
    cy = py + c // 2
    dx, dy    = direction
    perp_x    = -dy
    perp_y    =  dx

    r = c // 4
    pygame.draw.rect(screen, MB, (px + 2, py + 2, c - 4, c - 4), border_radius=r)
    pygame.draw.rect(screen, MD, (px + c // 3, py + c // 3,
                                   c * 2 // 3 - 4, c * 2 // 3 - 4), border_radius=r // 2)
    fur_strokes(screen, px, py, seed=11, count=12)

    ear_cx = int(cx - dx * c // 4 + perp_x * c // 3)
    ear_cy = int(cy - dy * c // 4 + perp_y * c // 3)
    pygame.draw.ellipse(screen, MB,
                        (ear_cx - c // 6, ear_cy - c // 6, c // 3, c // 3))
    pygame.draw.ellipse(screen, SKIN_C,
                        (ear_cx - c // 10, ear_cy - c // 10, c // 5, c // 5))

    e_cx = int(cx + dx * c // 5 - perp_x * c // 6)
    e_cy = int(cy + dy * c // 5 - perp_y * c // 6)
    fcirc(screen, EYE_W,           e_cx,          e_cy,          c // 8)
    fcirc(screen, EYE_P,           e_cx + dx + 1, e_cy + dy + 1, c // 13)
    fcirc(screen, (255, 255, 255), e_cx + 2,      e_cy - 2,      max(1, c // 22))

    for sign in (1, -1):
        sx = cx + dx * c // 3 + sign * perp_x * c // 8
        sy = cy + dy * c // 3 + sign * perp_y * c // 8
        pts = []
        for i in range(10):
            t  = i / 9.0
            tx = sx + dx * t * c * 0.65 + sign * perp_x * t * c * 0.50
            ty = sy + dy * t * c * 0.65 + sign * perp_y * t * c * 0.50
            pts.append((int(tx), int(ty)))
        pygame.draw.lines(screen, TUSK_C, False, pts, 4)
        pygame.draw.lines(screen, (236, 224, 170), False, pts, 2)
        fcirc(screen, (240, 232, 180), pts[-1][0], pts[-1][1], 3)

    trunk_pts = []
    for i in range(9):
        t      = i / 8.0
        wobble = math.sin(t * math.pi * 1.6) * c * 0.13 * (1 - t * 0.6)
        tx     = cx + dx * (c // 2 + t * c * 0.58) + perp_x * wobble
        ty     = cy + dy * (c // 2 + t * c * 0.58) + perp_y * wobble
        trunk_pts.append((int(tx), int(ty)))
    pygame.draw.lines(screen, SKIN_C, False, trunk_pts, max(4, c // 8))
    fcirc(screen, (75, 45, 18),   trunk_pts[-1][0],     trunk_pts[-1][1],     c // 10)
    fcirc(screen, (105, 66, 28),  trunk_pts[-1][0] - 1, trunk_pts[-1][1] - 1, c // 15)


# ── Misc draw ─────────────────────────────────────────────────────────────────

def draw_grid(screen):
    for x in range(0, W + 1, CELL):
        pygame.draw.line(screen, GRID_C, (x, 0), (x, GH))
    for y in range(0, GH + 1, CELL):
        pygame.draw.line(screen, GRID_C, (0, y), (W, y))


def draw_centered(surface, font, text, y, color=TEXT_C):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(W // 2, y))
    surface.blit(surf, rect)


def dark_overlay(screen):
    ov = pygame.Surface((W, GH), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 155))
    screen.blit(ov, (0, 0))


# ── UI helpers ────────────────────────────────────────────────────────────────

def make_rect(cx, cy, w=300, h=54):
    """Return a Rect centered at (cx, cy)."""
    return pygame.Rect(cx - w // 2, cy - h // 2, w, h)


def draw_btn(surf, font, text, rect, selected=False):
    hov = pygame.Rect(rect).collidepoint(pygame.mouse.get_pos())
    if selected:
        bg, border = BTN_SEL, TUSK_C
    elif hov:
        bg, border = BTN_HOV, GRID_C
    else:
        bg, border = BTN_BG, GRID_C
    pygame.draw.rect(surf, bg, rect, border_radius=10)
    pygame.draw.rect(surf, border, rect, 2, border_radius=10)
    lbl = font.render(text, True, TEXT_C)
    surf.blit(lbl, lbl.get_rect(center=pygame.Rect(rect).center))


def was_clicked(rect, event):
    return (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and pygame.Rect(rect).collidepoint(event.pos))


# ── Game helpers ──────────────────────────────────────────────────────────────

def random_food(snake):
    occupied = set(snake)
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in occupied:
            return pos


def new_game():
    cx, cy = COLS // 2, ROWS // 2
    snake  = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
    return snake, RIGHT, random_food(snake), 0


def get_speed(score, speed_key):
    base = min(22, FPS + score // 3)
    return max(4, int(base * SPEED_MULT[speed_key]))


# ── Menu screen ───────────────────────────────────────────────────────────────

def draw_menu(screen, fonts, cfg, lolly_surf):
    """Render main menu. Returns dict of button Rects."""
    font_big, font_med, font_small = fonts
    s = T[cfg["language"]]

    screen.fill(BG)
    # full-screen decorative grid
    for x in range(0, W + 1, CELL):
        pygame.draw.line(screen, GRID_C, (x, 0), (x, H))
    for y in range(0, H + 1, CELL):
        pygame.draw.line(screen, GRID_C, (0, y), (W, y))
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 120))
    screen.blit(ov, (0, 0))

    # decorative lollipops flanking the title
    screen.blit(lolly_surf, (W // 2 - 160 - CELL // 2, 155))
    screen.blit(lolly_surf, (W // 2 + 160 - CELL // 2, 155))

    draw_centered(screen, font_big, "MAMMOTH", 192, TUSK_C)

    rects = {
        "play":     make_rect(W // 2, 360),
        "settings": make_rect(W // 2, 438),
        "quit":     make_rect(W // 2, 516),
    }
    draw_btn(screen, font_med, s["play"],        rects["play"])
    draw_btn(screen, font_med, s["settings_btn"], rects["settings"])
    draw_btn(screen, font_med, s["quit"],         rects["quit"])
    return rects


# ── Settings screen ───────────────────────────────────────────────────────────

def draw_settings(screen, fonts, cfg):
    """Render settings screen. Returns dict of button Rects."""
    font_big, font_med, font_small = fonts
    lang = cfg["language"]
    s = T[lang]

    screen.fill(BG)
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 80))
    screen.blit(ov, (0, 0))

    draw_centered(screen, font_big, s["settings_btn"], 110, TUSK_C)
    pygame.draw.line(screen, GRID_C, (W // 4, 168), (W * 3 // 4, 168), 1)

    rects = {}
    LABEL_RIGHT = 300   # right edge of row labels
    # button center-x positions for 2-btn and 3-btn rows
    CENTERS_2 = [560, 700]
    CENTERS_3 = [460, 600, 740]

    def settings_row(y, label_key, btn_specs, use_small=False):
        lbl = font_med.render(s[label_key], True, TEXT_C)
        screen.blit(lbl, lbl.get_rect(midright=(LABEL_RIGHT, y)))
        centers = CENTERS_3 if len(btn_specs) == 3 else CENTERS_2
        bw = 105 if len(btn_specs) == 3 else 120
        f = font_small if use_small else font_med
        for i, (key, text, selected) in enumerate(btn_specs):
            r = make_rect(centers[i], y, bw, 50)
            draw_btn(screen, f, text, r, selected=selected)
            rects[key] = r

    settings_row(285, "language_label", [
        ("lang_de", "DE", lang == "de"),
        ("lang_en", "EN", lang == "en"),
    ])
    settings_row(390, "speed_label", [
        ("speed_slow",   s["slow"],   cfg["speed"] == "slow"),
        ("speed_normal", s["normal"], cfg["speed"] == "normal"),
        ("speed_fast",   s["fast"],   cfg["speed"] == "fast"),
    ], use_small=True)
    settings_row(490, "grid_label", [
        ("grid_on",  s["on"],  cfg["show_grid"]),
        ("grid_off", s["off"], not cfg["show_grid"]),
    ])

    rects["back"] = make_rect(W // 2, 630)
    draw_btn(screen, font_med, s["back"], rects["back"])
    return rects


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mammoth")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 56, bold=True)
    font_med   = pygame.font.SysFont("Arial", 30)
    font_small = pygame.font.SysFont("Arial", 20)
    fonts = (font_big, font_med, font_small)

    body_surf  = make_body_surf()
    lolly_surf = make_lollipop_surf()

    cfg = {"language": "de", "speed": "normal", "show_grid": True}

    snake, direction, food, score = new_game()
    high_score  = 0
    pending_dir = direction
    state       = "menu"

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state in ("playing", "dead", "settings"):
                    state = "menu"
                elif state == "menu":
                    pygame.quit()
                    sys.exit()

        # ── Menu ──────────────────────────────────────────────────────────
        if state == "menu":
            btn = draw_menu(screen, fonts, cfg, lolly_surf)
            for event in events:
                if was_clicked(btn["play"], event):
                    snake, direction, food, score = new_game()
                    pending_dir = direction
                    state = "playing"
                elif was_clicked(btn["settings"], event):
                    state = "settings"
                elif was_clicked(btn["quit"], event):
                    pygame.quit()
                    sys.exit()

        # ── Settings ──────────────────────────────────────────────────────
        elif state == "settings":
            btn = draw_settings(screen, fonts, cfg)
            for event in events:
                if was_clicked(btn["lang_de"], event):      cfg["language"] = "de"
                elif was_clicked(btn["lang_en"], event):    cfg["language"] = "en"
                elif was_clicked(btn["speed_slow"], event): cfg["speed"] = "slow"
                elif was_clicked(btn["speed_normal"], event): cfg["speed"] = "normal"
                elif was_clicked(btn["speed_fast"], event): cfg["speed"] = "fast"
                elif was_clicked(btn["grid_on"], event):    cfg["show_grid"] = True
                elif was_clicked(btn["grid_off"], event):   cfg["show_grid"] = False
                elif was_clicked(btn["back"], event):       state = "menu"

        # ── Playing / Dead ────────────────────────────────────────────────
        else:
            s = T[cfg["language"]]

            # game logic
            if state == "playing":
                direction = pending_dir
                hx, hy   = snake[0]
                dx, dy   = direction
                new_head = (hx + dx, hy + dy)

                if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS) \
                        or new_head in snake:
                    high_score = max(high_score, score)
                    state = "dead"
                else:
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        food = random_food(snake)
                    else:
                        snake.pop()

            # key input
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if state == "dead":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            snake, direction, food, score = new_game()
                            pending_dir = direction
                            state = "playing"
                    elif state == "playing":
                        nd = {
                            pygame.K_UP: UP,    pygame.K_w: UP,
                            pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                            pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                            pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
                        }.get(event.key)
                        if nd and nd != OPPOSITES[direction]:
                            pending_dir = nd

            # draw game
            screen.fill(BG)
            if cfg["show_grid"]:
                draw_grid(screen)

            for seg in reversed(snake[1:]):
                screen.blit(body_surf, (seg[0] * CELL, seg[1] * CELL))
            if snake:
                draw_head(screen, snake[0][0], snake[0][1], direction)
            screen.blit(lolly_surf, (food[0] * CELL, food[1] * CELL))

            # HUD
            pygame.draw.rect(screen, HUD_C, (0, GH, W, H - GH))
            pygame.draw.line(screen, GRID_C, (0, GH), (W, GH), 1)
            hud = font_small.render(
                f"{s['lollies']}:  {score}      {s['record']}:  {high_score}",
                True, TEXT_C)
            screen.blit(hud, (16, GH + 16))

            # dead overlay
            if state == "dead":
                dark_overlay(screen)
                draw_centered(screen, font_big,   s["game_over"],              GH // 2 - 65, PINK)
                draw_centered(screen, font_med,   s["score_msg"].format(score), GH // 2 + 10)
                draw_centered(screen, font_small, s["restart_hint"],            GH // 2 + 52)

        pygame.display.flip()
        clock.tick(get_speed(score, cfg["speed"]) if state == "playing" else 60)


if __name__ == "__main__":
    main()
