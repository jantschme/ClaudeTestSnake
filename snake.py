import pygame
import pygame.gfxdraw
import random
import sys
import math

# ── Config ────────────────────────────────────────────────────────────────────
CELL  = 44
COLS  = 20
ROWS  = 16
W     = COLS * CELL
GH    = ROWS * CELL
H     = GH + 54
FPS   = 10

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = ( 20,  36,  20)
GRID_C   = ( 30,  48,  30)
MB       = (112,  74,  36)   # mammoth body
MD       = ( 78,  50,  20)   # dark shade
MF       = (162, 118,  64)   # fur highlights
TUSK_C   = (252, 246, 200)   # ivory
SKIN_C   = ( 92,  58,  24)   # trunk skin
EYE_W    = (242, 230, 210)   # eye white
EYE_P    = ( 15,  10,   4)   # pupil
PINK     = (255,  88, 165)   # lollipop
PINK_H   = (255, 205, 232)   # highlight
PINK_D   = (200,  40, 120)   # shadow
STICK_C  = (200, 168, 128)   # stick
TEXT_C   = (228, 232, 220)
HUD_C    = ( 12,  22,  12)

RIGHT = ( 1,  0)
LEFT  = (-1,  0)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


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
    # inner shade
    pygame.draw.rect(s, MD, (c // 3, c // 3, c * 2 // 3 - 4, c * 2 // 3 - 4), border_radius=r // 2)
    fur_strokes(s, 0, 0, seed=42)
    return s


def make_lollipop_surf():
    c  = CELL
    s  = pygame.Surface((c, c), pygame.SRCALPHA)
    cr = c // 3
    cx = c // 2
    cy = c // 3

    # stick
    pygame.draw.line(s, STICK_C, (cx, cy + cr - 1), (cx, c - 3), 4)
    pygame.draw.line(s, (230, 200, 158), (cx - 1, cy + cr - 1), (cx - 1, c - 3), 1)

    # candy shadow
    fcirc(s, PINK_D, cx + 3, cy + 3, cr)
    # candy base
    fcirc(s, PINK, cx, cy, cr)
    # swirl arcs
    pygame.draw.arc(s, (255, 255, 255),
                    (cx - cr + 5, cy - cr + 5, (cr - 5) * 2, (cr - 5) * 2),
                    math.pi * 0.3, math.pi * 1.25, 3)
    pygame.draw.arc(s, (255, 255, 255),
                    (cx - cr // 2 + 3, cy - cr // 2 + 3, (cr // 2 - 3) * 2, (cr // 2 - 3) * 2),
                    math.pi * 1.1, math.pi * 2.1, 2)
    # highlight
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

    # ── base rounded rect ──────────────────────────────────────────
    r = c // 4
    pygame.draw.rect(screen, MB, (px + 2, py + 2, c - 4, c - 4), border_radius=r)
    pygame.draw.rect(screen, MD, (px + c // 3, py + c // 3,
                                   c * 2 // 3 - 4, c * 2 // 3 - 4), border_radius=r // 2)
    fur_strokes(screen, px, py, seed=11, count=12)

    # ── ear (back-perp side) ───────────────────────────────────────
    ear_cx = int(cx - dx * c // 4 + perp_x * c // 3)
    ear_cy = int(cy - dy * c // 4 + perp_y * c // 3)
    pygame.draw.ellipse(screen, MB,
                        (ear_cx - c // 6, ear_cy - c // 6, c // 3, c // 3))
    pygame.draw.ellipse(screen, SKIN_C,
                        (ear_cx - c // 10, ear_cy - c // 10, c // 5, c // 5))

    # ── eye ────────────────────────────────────────────────────────
    e_cx = int(cx + dx * c // 5 - perp_x * c // 6)
    e_cy = int(cy + dy * c // 5 - perp_y * c // 6)
    fcirc(screen, EYE_W,          e_cx,         e_cy,         c // 8)
    fcirc(screen, EYE_P,          e_cx + dx + 1, e_cy + dy + 1, c // 13)
    fcirc(screen, (255, 255, 255), e_cx + 2,     e_cy - 2,     max(1, c // 22))

    # ── tusks (two, curving forward and outward) ───────────────────
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

    # ── trunk (extends from front, slight curve) ───────────────────
    trunk_pts = []
    for i in range(9):
        t      = i / 8.0
        wobble = math.sin(t * math.pi * 1.6) * c * 0.13 * (1 - t * 0.6)
        tx     = cx + dx * (c // 2 + t * c * 0.58) + perp_x * wobble
        ty     = cy + dy * (c // 2 + t * c * 0.58) + perp_y * wobble
        trunk_pts.append((int(tx), int(ty)))
    pygame.draw.lines(screen, SKIN_C, False, trunk_pts, max(4, c // 8))
    fcirc(screen, (75, 45, 18),  trunk_pts[-1][0],     trunk_pts[-1][1],     c // 10)
    fcirc(screen, (105, 66, 28), trunk_pts[-1][0] - 1, trunk_pts[-1][1] - 1, c // 15)


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


def get_speed(score):
    return min(22, FPS + score // 3)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mammoth")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 56, bold=True)
    font_med   = pygame.font.SysFont("Arial", 30)
    font_small = pygame.font.SysFont("Arial", 20)

    body_surf  = make_body_surf()
    lolly_surf = make_lollipop_surf()

    snake, direction, food, score = new_game()
    high_score  = 0
    pending_dir = direction
    state       = "start"

    while True:
        # ── Events ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state in ("start", "dead"):
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
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # ── Logic ─────────────────────────────────────────────────────────
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

        # ── Draw ──────────────────────────────────────────────────────────
        screen.fill(BG)
        draw_grid(screen)

        # body (back → front, skip head)
        for seg in reversed(snake[1:]):
            screen.blit(body_surf, (seg[0] * CELL, seg[1] * CELL))

        # head
        if snake:
            draw_head(screen, snake[0][0], snake[0][1], direction)

        # lollipop
        screen.blit(lolly_surf, (food[0] * CELL, food[1] * CELL))

        # HUD
        pygame.draw.rect(screen, HUD_C, (0, GH, W, H - GH))
        pygame.draw.line(screen, GRID_C, (0, GH), (W, GH), 1)
        hud = font_small.render(
            f"Lollies:  {score}      Rekord:  {high_score}", True, TEXT_C)
        screen.blit(hud, (16, GH + 16))

        # overlays
        if state == "start":
            dark_overlay(screen)
            draw_centered(screen, font_big,   "MAMMOTH",                        GH // 2 - 65, TUSK_C)
            draw_centered(screen, font_med,   "Leertaste zum Starten",          GH // 2 + 10)
            draw_centered(screen, font_small, "Pfeiltasten oder WASD bewegen",  GH // 2 + 52)

        elif state == "dead":
            dark_overlay(screen)
            draw_centered(screen, font_big,   "AUSGESTORBEN",                   GH // 2 - 65, PINK)
            draw_centered(screen, font_med,   f"Lollies gegessen: {score}",     GH // 2 + 10)
            draw_centered(screen, font_small, "Leertaste für neues Spiel",      GH // 2 + 52)

        pygame.display.flip()
        clock.tick(get_speed(score))


if __name__ == "__main__":
    main()
