import pygame
import pygame.gfxdraw
import random
import sys
import math
import json
import array
import pathlib

# ── Config ────────────────────────────────────────────────────────────────────
CELL  = 64
COLS  = 16
ROWS  = 12
W     = COLS * CELL          # 1024
GH    = ROWS * CELL          # 768
H     = GH + 60              # 828
FPS   = 8
RENDER_FPS = 60
TIME_ATTACK_SECS = 60

# ── Colors ────────────────────────────────────────────────────────────────────
BG         = (  8,  12,  22)   # deep navy
GRID_C     = ( 18,  28,  52)   # dark slate blue
MB         = (112,  74,  36)   # mammoth brown (unchanged)
MD         = ( 78,  50,  20)
MF         = (162, 118,  64)
TUSK_C     = (252, 246, 200)   # mammoth tusk (unchanged)
SKIN_C     = ( 92,  58,  24)
EYE_W      = (242, 230, 210)
EYE_P      = ( 15,  10,   4)
PINK       = (255,  88, 165)
PINK_H     = (255, 205, 232)
PINK_D     = (200,  40, 120)
STICK_C    = (200, 168, 128)
TEXT_C     = (220, 228, 245)   # cool white
HUD_C      = (  5,   8,  18)   # near-black navy
BTN_BG     = ( 18,  32,  68)
BTN_HOV    = ( 30,  55, 105)
BTN_SEL    = ( 35,  80, 190)
OBSTACLE_C = ( 45,  55, 100)
BUNNY_BODY = (200, 195, 195)
BUNNY_EAR  = (230, 150, 160)
BUNNY_NOSE = (255, 150, 160)
BEAR_BODY  = (160, 100,  50)
BEAR_LIGHT = (200, 150, 100)
BEAR_NOSE  = ( 60,  40,  20)
CARROT_C   = (255, 130,  30)
LEAF_C     = ( 50, 180,  50)
HONEY_C    = (240, 200,  40)
POT_C      = (180, 120,  60)
ACCENT     = ( 80, 150, 255)   # main blue accent
ACCENT_DIM = ( 40,  80, 160)
TITLE_C    = (180, 210, 255)   # title/highlights
BTN_GLOW   = ( 60, 130, 255)

RIGHT = ( 1,  0)
LEFT  = (-1,  0)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
SPEED_MULT = {"slow": 0.55, "normal": 0.80, "fast": 1.20}
CHARACTERS = ["mammoth", "bunny", "bear"]
CHAR_FOOD  = {"mammoth": "lolly", "bunny": "carrot", "bear": "honey"}

BG_STYLE_NAMES = ["grid", "space", "deep_ocean", "neon_city"]
_hover_t = {}  # module-level hover easing state for menu cards

# ── Save path ─────────────────────────────────────────────────────────────────
SAVE_DIR  = pathlib.Path.home() / "Library" / "Application Support" / "Mammoth"
SAVE_FILE = SAVE_DIR / "save.json"

# ── Translations ──────────────────────────────────────────────────────────────
T = {
    "de": {
        "play":              "SPIELEN",
        "settings_btn":      "EINSTELLUNGEN",
        "quit":              "BEENDEN",
        "language_label":    "Sprache",
        "speed_label":       "Geschwindigkeit",
        "grid_label":        "Raster",
        "sound_label":       "Sound",
        "back":              "ZURÜCK",
        "slow":              "LANGSAM",
        "normal":            "NORMAL",
        "fast":              "SCHNELL",
        "on":                "AN",
        "off":               "AUS",
        "game_over":         "AUSGESTORBEN",
        "time_up":           "ZEIT ABGELAUFEN",
        "score_msg":         "Gegessen: {}",
        "restart_hint":      "LEERTASTE = Neu  |  ESC = Menü",
        "lollies":           "Punkte",
        "record":            "Rekord",
        "char_select":       "CHARAKTER WÄHLEN",
        "mode_select":       "SPIELMODUS",
        "mode_classic":      "KLASSISCH",
        "mode_timeattack":   "ZEITANGRIFF",
        "mode_zen":          "ZEN",
        "mode_obstacles":    "HINDERNISSE",
        "mode_classic_d":    "Standard Snake",
        "mode_timeattack_d": "60 Sek – max Punkte",
        "mode_zen_d":        "Wände = Teleport",
        "mode_obstacles_d":  "Zufällige Blöcke",
        "pause":             "PAUSE",
        "pause_hint":        "P = Weiter  |  ESC = Menü",
        "time":              "Zeit",
        "char_mammoth":      "Mammuth",
        "char_bunny":        "Hase",
        "char_bear":         "Bär",
        "bg_style_label":    "Hintergrund",
        "bg_grid":           "RASTER",
        "bg_space":          "WELTRAUM",
        "bg_ocean":          "OZEAN",
        "bg_neon":           "NEON",
    },
    "en": {
        "play":              "PLAY",
        "settings_btn":      "SETTINGS",
        "quit":              "QUIT",
        "language_label":    "Language",
        "speed_label":       "Speed",
        "grid_label":        "Grid",
        "sound_label":       "Sound",
        "back":              "BACK",
        "slow":              "SLOW",
        "normal":            "NORMAL",
        "fast":              "FAST",
        "on":                "ON",
        "off":               "OFF",
        "game_over":         "EXTINCT",
        "time_up":           "TIME'S UP",
        "score_msg":         "Eaten: {}",
        "restart_hint":      "SPACE = New Game  |  ESC = Menu",
        "lollies":           "Score",
        "record":            "Record",
        "char_select":       "CHOOSE CHARACTER",
        "mode_select":       "GAME MODE",
        "mode_classic":      "CLASSIC",
        "mode_timeattack":   "TIME ATTACK",
        "mode_zen":          "ZEN",
        "mode_obstacles":    "OBSTACLES",
        "mode_classic_d":    "Standard Snake",
        "mode_timeattack_d": "60 sec – max score",
        "mode_zen_d":        "Walls = Teleport",
        "mode_obstacles_d":  "Random blocks",
        "pause":             "PAUSE",
        "pause_hint":        "P = Resume  |  ESC = Menu",
        "time":              "Time",
        "char_mammoth":      "Mammoth",
        "char_bunny":        "Bunny",
        "char_bear":         "Bear",
        "bg_style_label":    "Background",
        "bg_grid":           "GRID",
        "bg_space":          "SPACE",
        "bg_ocean":          "OCEAN",
        "bg_neon":           "NEON",
    },
}


# ── Persistence ───────────────────────────────────────────────────────────────

def load_save():
    defaults = {
        "high_scores":    {},
        "language":       "de",
        "speed":          "normal",
        "show_grid":      True,
        "sound":          True,
        "last_character": "mammoth",
        "last_mode":      "classic",
        "bg_style":       "grid",
    }
    try:
        if SAVE_FILE.exists():
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            defaults.update(data)
    except Exception:
        pass
    return defaults


def write_save(save):
    try:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        with open(SAVE_FILE, "w") as f:
            json.dump(save, f, indent=2)
    except Exception:
        pass


def hs_key(character, mode):
    return f"{character}_{mode}"


# ── Sound ─────────────────────────────────────────────────────────────────────

def _gen_tone(freq, duration, volume=0.3, sr=22050):
    n = int(sr * duration)
    buf = array.array("h", [0] * n)
    mv = int(32767 * volume)
    for i in range(n):
        fade = min(1.0, (n - i) / max(1, n * 0.1))
        buf[i] = int(mv * math.sin(2 * math.pi * freq * i / sr) * fade)
    return pygame.mixer.Sound(buffer=buf)


def _gen_sweep(f0, f1, duration, volume=0.3, sr=22050):
    n = int(sr * duration)
    buf = array.array("h", [0] * n)
    mv = int(32767 * volume)
    for i in range(n):
        freq = f0 + (f1 - f0) * i / n
        fade = min(1.0, (n - i) / max(1, n * 0.1))
        buf[i] = int(mv * math.sin(2 * math.pi * freq * i / sr) * fade)
    return pygame.mixer.Sound(buffer=buf)


def init_sounds():
    sounds = {}
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        sounds["eat"]   = _gen_tone(600, 0.08, 0.4)
        sounds["dead"]  = _gen_sweep(300, 80, 0.35, 0.35)
        sounds["click"] = _gen_tone(800, 0.05, 0.25)
        sounds["pause"] = _gen_tone(400, 0.06, 0.2)
    except Exception:
        pass
    return sounds


def play_snd(sounds, key, save):
    if save.get("sound") and key in sounds:
        try:
            sounds[key].play()
        except Exception:
            pass


# ── Easing ────────────────────────────────────────────────────────────────────

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3

def ease_in_out_quad(t):
    t = max(0.0, min(1.0, t))
    return 2*t*t if t < 0.5 else 1 - (-2*t+2)**2/2

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2*t)


# ── Drawing helpers ───────────────────────────────────────────────────────────

def fcirc(surf, color, cx, cy, r):
    cx, cy, r = int(cx), int(cy), int(r)
    if r <= 0:
        return
    pygame.gfxdraw.filled_circle(surf, cx, cy, r, color)
    pygame.gfxdraw.aacircle(surf, cx, cy, r, color)


def fcirc_alpha(surf, color, cx, cy, r):
    r = max(1, int(r))
    tmp = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
    pygame.gfxdraw.filled_circle(tmp, r+1, r+1, r, color)
    pygame.gfxdraw.aacircle(tmp, r+1, r+1, r, color)
    surf.blit(tmp, (int(cx)-r-1, int(cy)-r-1))


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


# ── Body surfaces ─────────────────────────────────────────────────────────────

def make_body_surf(char="mammoth"):
    c = CELL
    s = pygame.Surface((c, c), pygame.SRCALPHA)
    r = c // 4
    if char == "mammoth":
        pygame.draw.rect(s, MB, (2, 2, c-4, c-4), border_radius=r)
        pygame.draw.rect(s, MD, (c//3, c//3, c*2//3-4, c*2//3-4), border_radius=r//2)
        fur_strokes(s, 0, 0, seed=42)
    elif char == "bunny":
        pygame.draw.rect(s, BUNNY_BODY, (2, 2, c-4, c-4), border_radius=r)
        pygame.draw.rect(s, (170,165,165), (c//3, c//3, c*2//3-4, c*2//3-4), border_radius=r//2)
    else:  # bear
        pygame.draw.rect(s, BEAR_BODY, (2, 2, c-4, c-4), border_radius=r)
        pygame.draw.rect(s, (130,80,30), (c//3, c//3, c*2//3-4, c*2//3-4), border_radius=r//2)
        fur_strokes(s, 0, 0, seed=99)
    return s


# ── Animal heads ──────────────────────────────────────────────────────────────

def draw_head_mammoth(screen, px, py, direction):
    c  = CELL
    cx, cy = px + c//2, py + c//2
    dx, dy = direction
    px2, py2 = -dy, dx  # perp

    r = c // 4
    # 3-layer base
    pygame.draw.rect(screen, (78, 48, 18), (px+4, py+5, c-8, c-8), border_radius=r)
    pygame.draw.rect(screen, MB, (px+2, py+2, c-4, c-4), border_radius=r)
    pygame.draw.rect(screen, MD, (px+c//3, py+c//3, c*2//3-4, c*2//3-4), border_radius=r//2)
    fur_strokes(screen, px, py, seed=11, count=12)
    # Top highlight
    fcirc_alpha(screen, (220, 180, 100, 45), cx - dx*c//6, cy - dy*c//6, c//5)

    ear_cx = int(cx - dx*c//4 + px2*c//3)
    ear_cy = int(cy - dy*c//4 + py2*c//3)
    pygame.draw.ellipse(screen, MB, (ear_cx-c//6, ear_cy-c//6, c//3, c//3))
    pygame.draw.ellipse(screen, SKIN_C, (ear_cx-c//10, ear_cy-c//10, c//5, c//5))

    ecx = int(cx + dx*c//5 - px2*c//6)
    ecy = int(cy + dy*c//5 - py2*c//6)
    fcirc(screen, EYE_W, ecx, ecy, c//8)
    # Iris ring
    fcirc(screen, (140, 90, 40), ecx+dx, ecy+dy, c//11)
    fcirc(screen, EYE_P, ecx+dx+1, ecy+dy+1, c//14)
    fcirc(screen, (255,255,255), ecx+2, ecy-2, max(1, c//22))
    fcirc(screen, (255,255,255), ecx-1, ecy+2, max(1, c//30))

    for sign in (1, -1):
        sx = cx + dx*c//3 + sign*px2*c//8
        sy = cy + dy*c//3 + sign*py2*c//8
        pts = []
        for i in range(10):
            t = i / 9.0
            pts.append((int(sx + dx*t*c*0.65 + sign*px2*t*c*0.50),
                         int(sy + dy*t*c*0.65 + sign*py2*t*c*0.50)))
        # Shadow line first
        shadow_pts = [(x+2, y+2) for x, y in pts]
        pygame.draw.lines(screen, (160, 140, 80), False, shadow_pts, 3)
        pygame.draw.lines(screen, TUSK_C, False, pts, 4)
        pygame.draw.lines(screen, (255, 252, 220), False, pts, 2)
        fcirc(screen, (240,232,180), pts[-1][0], pts[-1][1], 3)

    trunk_pts = []
    for i in range(9):
        t = i / 8.0
        wobble = math.sin(t * math.pi * 1.6) * c * 0.13 * (1 - t*0.6)
        trunk_pts.append((int(cx + dx*(c//2 + t*c*0.58) + px2*wobble),
                           int(cy + dy*(c//2 + t*c*0.58) + py2*wobble)))
    pygame.draw.lines(screen, SKIN_C, False, trunk_pts, max(4, c//8))
    # Highlight line offset
    hl_pts = [(x - dy*2, y + dx*2) for x, y in trunk_pts]
    pygame.draw.lines(screen, MF, False, hl_pts, max(1, c//16))
    fcirc(screen, (75,45,18),  trunk_pts[-1][0],   trunk_pts[-1][1],   c//10)
    fcirc(screen, (105,66,28), trunk_pts[-1][0]-1, trunk_pts[-1][1]-1, c//15)
    fcirc(screen, (180,130,80), trunk_pts[-1][0]-2, trunk_pts[-1][1]-2, max(1, c//22))


def draw_head_bunny(screen, px, py, direction):
    c  = CELL
    cx, cy = px + c//2, py + c//2
    dx, dy = direction
    px2, py2 = -dy, dx

    # Shadow disc + main + highlight
    fcirc(screen, (160, 150, 150), cx+2, cy+3, c//3)
    fcirc(screen, BUNNY_BODY, cx, cy, c//3)
    fcirc_alpha(screen, (255, 255, 255, 40), cx - dx*c//6, cy - dy*c//6, c//6)

    # Ears as polygons (taper from base to tip)
    for sign in (1, -1):
        bx = int(cx - dx*c//4 + sign*px2*c//5)
        by = int(cy - dy*c//4 + sign*py2*c//5)
        tx = int(bx - dx*c*0.6)
        ty = int(by - dy*c*0.6)
        # perpendicular to ear direction
        ear_dx, ear_dy = tx-bx, ty-by
        ear_len = math.hypot(ear_dx, ear_dy) or 1
        ear_nx, ear_ny = -ear_dy/ear_len, ear_dx/ear_len
        # Tapered polygon (wide at base, narrow at tip)
        base_w, tip_w = 7, 3
        ear_pts = [
            (int(bx + ear_nx*base_w), int(by + ear_ny*base_w)),
            (int(bx - ear_nx*base_w), int(by - ear_ny*base_w)),
            (int(tx - ear_nx*tip_w),  int(ty - ear_ny*tip_w)),
            (int(tx + ear_nx*tip_w),  int(ty + ear_ny*tip_w)),
        ]
        pygame.draw.polygon(screen, BUNNY_BODY, ear_pts)
        # Pink inner strip
        inner_pts = [
            (int(bx + ear_nx*3), int(by + ear_ny*3)),
            (int(bx - ear_nx*3), int(by - ear_ny*3)),
            (int(tx - ear_nx*1), int(ty - ear_ny*1)),
            (int(tx + ear_nx*1), int(ty + ear_ny*1)),
        ]
        pygame.draw.polygon(screen, BUNNY_EAR, inner_pts)

    # Cheek blush
    fcirc_alpha(screen, (255, 150, 180, 35), int(cx - px2*c//5), int(cy - py2*c//5), c//7)

    # Eye with pink iris ring
    ecx = int(cx + dx*c//5 - px2*c//7)
    ecy = int(cy + dy*c//5 - py2*c//7)
    fcirc(screen, EYE_W, ecx, ecy, c//9)
    fcirc(screen, (220, 80, 120), ecx+dx, ecy+dy, c//12)
    fcirc(screen, (180,50,80), ecx+dx, ecy+dy, c//15)
    fcirc(screen, (255,255,255), ecx+2, ecy-2, max(1, c//22))

    # Nose + whiskers
    nx = int(cx + dx*c//2.8)
    ny = int(cy + dy*c//2.8)
    fcirc(screen, BUNNY_NOSE, nx, ny, c//9)
    for sign in (1, -1):
        wx = int(nx - dx*c//5 + sign*px2*c//3)
        wy = int(ny - dy*c//5 + sign*py2*c//3)
        pygame.draw.line(screen, (200,180,180), (nx, ny), (wx, wy), 1)


def draw_head_bear(screen, px, py, direction):
    c  = CELL
    cx, cy = px + c//2, py + c//2
    dx, dy = direction
    px2, py2 = -dy, dx

    # Shadow disc + main + ambient highlight
    fcirc(screen, (110, 65, 25), cx+2, cy+3, int(c*0.42))
    fcirc(screen, BEAR_BODY, cx, cy, int(c*0.42))
    fcirc_alpha(screen, (220, 170, 110, 40), cx - dx*c//6, cy - dy*c//6, c//5)

    # Round ears
    for sign in (1, -1):
        ecx = int(cx - dx*c//3 + sign*px2*c//3)
        ecy = int(cy - dy*c//3 + sign*py2*c//3)
        fcirc(screen, BEAR_BODY, ecx, ecy, c//6)
        fcirc(screen, (130,70,30), ecx, ecy, c//10)

    # Muzzle with shadow + highlight
    mx = int(cx + dx*c//4)
    my = int(cy + dy*c//4)
    fcirc(screen, (150, 105, 60), mx+1, my+2, c//5)
    fcirc(screen, BEAR_LIGHT, mx, my, c//5)
    fcirc_alpha(screen, (255, 230, 190, 50), mx - dx*3, my - dy*3, c//9)

    # Nose: darker shadow + main + specular
    nnx = int(cx + dx*c//2.5)
    nny = int(cy + dy*c//2.5)
    fcirc(screen, (30, 20, 10), nnx+1, nny+1, c//9)
    fcirc(screen, BEAR_NOSE, nnx, nny, c//10)
    fcirc(screen, (255, 255, 255), nnx-2, nny-2, max(1, c//22))

    # Eyes (two) with amber iris
    for sign in (1, -1):
        ecx = int(cx + dx*c//6 + sign*px2*c//5)
        ecy = int(cy + dy*c//6 + sign*py2*c//5)
        fcirc(screen, EYE_W, ecx, ecy, c//9)
        fcirc(screen, (180, 120, 30), ecx+dx, ecy+dy, c//12)
        fcirc(screen, EYE_P, ecx+dx, ecy+dy, c//15)
        fcirc(screen, (255,255,255), ecx+2, ecy-2, max(1, c//22))


def draw_head(screen, px, py, direction, character="mammoth"):
    if character == "bunny":
        draw_head_bunny(screen, px, py, direction)
    elif character == "bear":
        draw_head_bear(screen, px, py, direction)
    else:
        draw_head_mammoth(screen, px, py, direction)


# ── Food surfaces ─────────────────────────────────────────────────────────────

def make_lolly_surf():
    c = CELL
    s = pygame.Surface((c, c), pygame.SRCALPHA)
    cr, cx, cy = c//3, c//2, c//3
    pygame.draw.line(s, STICK_C, (cx, cy+cr-1), (cx, c-3), 4)
    pygame.draw.line(s, (230,200,158), (cx-1, cy+cr-1), (cx-1, c-3), 1)
    fcirc(s, PINK_D, cx+3, cy+3, cr)
    fcirc(s, PINK, cx, cy, cr)
    pygame.draw.arc(s, (255,255,255), (cx-cr+5, cy-cr+5, (cr-5)*2, (cr-5)*2),
                    math.pi*0.3, math.pi*1.25, 3)
    fcirc(s, PINK_H, cx-cr//3, cy-cr//3, cr//3)
    return s


def make_carrot_surf():
    c = CELL
    s = pygame.Surface((c, c), pygame.SRCALPHA)
    cx = c // 2
    pts = [(cx-c//4, 8), (cx+c//4, 8), (cx, c-6)]
    pygame.draw.polygon(s, CARROT_C, pts)
    for i in range(2, c-10, 7):
        lx = max(2, int(c//4 * (1 - i/c)))
        pygame.draw.line(s, (220,100,20), (cx-lx, 8+i), (cx+lx, 8+i), 1)
    for sign in (-1, 0, 1):
        pygame.draw.line(s, LEAF_C, (cx+sign*4, 8), (cx+sign*10, -2), 3)
    return s


def make_honeypot_surf():
    c = CELL
    s = pygame.Surface((c, c), pygame.SRCALPHA)
    cx = c // 2
    pot = pygame.Rect(cx-c//3, c//3, c*2//3, c*2//3)
    pygame.draw.ellipse(s, POT_C, pot)
    pygame.draw.ellipse(s, (150,90,40), pot, 2)
    honey = pygame.Rect(cx-c//4, c//3-2, c//2, c//5)
    pygame.draw.ellipse(s, HONEY_C, honey)
    dx = cx + c//8
    pygame.draw.line(s, HONEY_C, (dx, c//3+c//5), (dx, c//3+c//5+8), 4)
    fcirc(s, HONEY_C, dx, c//3+c//5+8, 4)
    pygame.draw.rect(s, (150,90,40), (cx-c//3, c//3-4, c*2//3, 6), border_radius=3)
    return s


def make_food_surf(character):
    food = CHAR_FOOD.get(character, "lolly")
    if food == "carrot":
        return make_carrot_surf()
    elif food == "honey":
        return make_honeypot_surf()
    return make_lolly_surf()


def food_color(character):
    food = CHAR_FOOD.get(character, "lolly")
    return CARROT_C if food == "carrot" else HONEY_C if food == "honey" else PINK


# ── Particles ─────────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.pi*2)
        speed = random.uniform(1.5, 4.5)
        self.x, self.y   = float(x), float(y)
        self.vx, self.vy = math.cos(angle)*speed, math.sin(angle)*speed - 1.0
        self.color        = color
        self.lifetime     = random.randint(14, 24)
        self.age          = 0
        self.size         = random.randint(3, 6)

    @property
    def alive(self):
        return self.age < self.lifetime


def emit_particles(pos, color, count=14):
    px = pos[0]*CELL + CELL//2
    py = pos[1]*CELL + CELL//2
    return [Particle(px, py, color) for _ in range(count)]


def update_particles(particles):
    for p in particles:
        p.x += p.vx; p.y += p.vy
        p.vy += 0.18
        p.age += 1
    particles[:] = [p for p in particles if p.alive]


def draw_particles(screen, particles):
    for p in particles:
        alpha = max(0.0, 1.0 - p.age / p.lifetime)
        size  = max(1, int(p.size * alpha))
        surf  = pygame.Surface((size*2+2, size*2+2), pygame.SRCALPHA)
        fcirc(surf, (*p.color, int(255*alpha)), size+1, size+1, size)
        screen.blit(surf, (int(p.x)-size-1, int(p.y)-size-1))


# ── Misc draw ─────────────────────────────────────────────────────────────────

def draw_grid(screen):
    for x in range(0, W+1, CELL):
        pygame.draw.line(screen, GRID_C, (x, 0), (x, GH))
    for y in range(0, GH+1, CELL):
        pygame.draw.line(screen, GRID_C, (0, y), (W, y))


def draw_centered(surface, font, text, y, color=TEXT_C):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=(W//2, y)))


def dark_overlay(screen):
    ov = pygame.Surface((W, GH), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 155))
    screen.blit(ov, (0, 0))


# ── UI helpers ────────────────────────────────────────────────────────────────

def make_rect(cx, cy, w=300, h=54):
    return pygame.Rect(cx-w//2, cy-h//2, w, h)


def draw_btn(surf, font, text, rect, selected=False):
    r = pygame.Rect(rect)
    hov = r.collidepoint(pygame.mouse.get_pos())
    pressed = hov and pygame.mouse.get_pressed()[0]

    if not pressed:
        shadow_r = r.move(3, 3)
        sh = pygame.Surface((shadow_r.width, shadow_r.height), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0, 0, 0, 80), sh.get_rect(), border_radius=10)
        surf.blit(sh, shadow_r.topleft)

    draw_r = r.inflate(-4, -4) if pressed else r

    # Outer glow
    if hov or selected:
        glow_alpha = 75 if selected else 50
        gw, gh = draw_r.width + 10, draw_r.height + 10
        glow_surf = pygame.Surface((gw, gh), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*BTN_GLOW, glow_alpha), (0, 0, gw, gh), border_radius=13)
        surf.blit(glow_surf, (draw_r.x - 5, draw_r.y - 5))

    # Gradient fill
    bg_top = BTN_SEL if selected else (BTN_HOV if hov else BTN_BG)
    bg_bot = tuple(max(0, c - 22) for c in bg_top)
    grad_surf = pygame.Surface((draw_r.width, draw_r.height), pygame.SRCALPHA)
    for gy in range(draw_r.height):
        t = gy / max(1, draw_r.height - 1)
        gc = tuple(int(bg_top[k] + (bg_bot[k] - bg_top[k]) * t) for k in range(3))
        pygame.draw.line(grad_surf, (*gc, 255), (0, gy), (draw_r.width, gy))
    # Round the gradient corners via mask
    mask = pygame.Surface((draw_r.width, draw_r.height), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=10)
    grad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(grad_surf, draw_r.topleft)

    # Border
    border = ACCENT if selected else (TEXT_C if hov else GRID_C)
    pygame.draw.rect(surf, border, draw_r, 2, border_radius=10)

    # Top bevel highlight
    pygame.draw.line(surf, (255, 255, 255), (draw_r.x + 10, draw_r.y + 1),
                     (draw_r.right - 10, draw_r.y + 1), 1)

    # Text with shadow
    shadow_lbl = font.render(text, True, (0, 0, 0))
    surf.blit(shadow_lbl, shadow_lbl.get_rect(center=(draw_r.centerx + 1, draw_r.centery + 1)))
    lbl = font.render(text, True, TEXT_C)
    surf.blit(lbl, lbl.get_rect(center=draw_r.center))


def was_clicked(rect, event):
    return (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and pygame.Rect(rect).collidepoint(event.pos))


# ── Game helpers ──────────────────────────────────────────────────────────────

def random_food(snake, obstacles=None):
    occupied = set(snake) | (set(obstacles) if obstacles else set())
    while True:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if pos not in occupied:
            return pos


def random_obstacles(snake, count=12):
    occupied = set(snake)
    obs, attempts = [], 0
    while len(obs) < count and attempts < 300:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if pos not in occupied and pos not in obs:
            obs.append(pos)
        attempts += 1
    return obs


def new_game(mode="classic"):
    cx, cy = COLS//2, ROWS//2
    snake  = [(cx, cy), (cx-1, cy), (cx-2, cy)]
    obs    = random_obstacles(snake) if mode == "obstacles" else []
    return snake, RIGHT, random_food(snake, obs), 0, obs


def get_speed(score, speed_key):
    base = min(22, FPS + score//3)
    return max(4, int(base * SPEED_MULT[speed_key]))


# ── HUD ───────────────────────────────────────────────────────────────────────

def draw_hud(screen, font_small, save, score, character, mode, time_left):
    s  = T[save["language"]]
    hs = save["high_scores"].get(hs_key(character, mode), 0)
    pygame.draw.rect(screen, HUD_C, (0, GH, W, H-GH))
    pygame.draw.line(screen, GRID_C, (0, GH), (W, GH), 1)
    if mode == "timeattack":
        txt = f"{s['lollies']}: {score}   {s['time']}: {max(0, int(time_left))}s   {s['record']}: {hs}"
    else:
        txt = f"{s['lollies']}: {score}   {s['record']}: {hs}"
    hud = font_small.render(txt, True, TEXT_C)
    screen.blit(hud, (16, GH+16))


# ── Screen renderers ──────────────────────────────────────────────────────────

def draw_bg_grid(screen):
    screen.fill(BG)

    for x in range(0, W+1, CELL):
        pygame.draw.line(screen, GRID_C, (x, 0), (x, H))
    for y in range(0, H+1, CELL):
        pygame.draw.line(screen, GRID_C, (0, y), (W, y))

    diag_color = (20, 35, 65)
    diag_spacing = CELL * 2
    for x in range(-H, W, diag_spacing):
        pygame.draw.line(screen, diag_color, (x, 0), (x+H, H), 1)
    for x in range(0, W+H, diag_spacing):
        pygame.draw.line(screen, diag_color, (x, 0), (x-H, H), 1)

    grad = pygame.Surface((W, H), pygame.SRCALPHA)
    for y in range(H):
        edge_dist = min(y, H - y) / (H / 2)
        alpha = int(80 * (1.0 - edge_dist))
        pygame.draw.line(grad, (0, 0, 0, alpha), (0, y), (W, y))
    screen.blit(grad, (0, 0))

    random.seed(42)
    for i in range(12):
        spx = random.randint(0, W)
        spy = random.randint(0, H)
        size = random.randint(1, 3)
        sparkle_alpha = int(80 * (1.0 - abs(math.sin(pygame.time.get_ticks() / 500 + i)) * 0.5))
        spark = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(spark, (100, 160, 255, sparkle_alpha), (size, size), size)
        screen.blit(spark, (spx-size, spy-size))


def draw_bg_space(screen, static_surfs, t):
    screen.fill((4, 6, 14))
    if "stars_bg" in static_surfs:
        screen.blit(static_surfs["stars_bg"], (0, 0))
    if "nebula_bg" in static_surfs:
        screen.blit(static_surfs["nebula_bg"], (0, 0))
    # Animated twinkle stars
    rng = random.Random(77)
    for i in range(6):
        tx = rng.randint(50, W-50)
        ty = rng.randint(30, H-30)
        tr = 1 + rng.randint(0, 1)
        ta = int(120 + 100 * math.sin(t * 2.0 + i * 1.1))
        ts = pygame.Surface((tr*2+2, tr*2+2), pygame.SRCALPHA)
        pygame.draw.circle(ts, (200, 220, 255, ta), (tr+1, tr+1), tr)
        screen.blit(ts, (tx-tr-1, ty-tr-1))
    pygame.draw.rect(screen, GRID_C, (0, 0, W, H), 2)


def draw_bg_ocean(screen, static_surfs, t):
    if "ocean_bg" in static_surfs:
        screen.blit(static_surfs["ocean_bg"], (0, 0))
    else:
        screen.fill((5, 20, 45))
    # Animated caustic blobs
    rng = random.Random(13)
    for i in range(5):
        bx = rng.randint(100, W-100)
        by = rng.randint(80, GH-80)
        bx_off = int(30 * math.sin(t * 0.8 + i * 1.3))
        by_off = int(20 * math.sin(t * 1.1 + i * 0.9))
        br = 28 + int(12 * math.sin(t * 0.6 + i * 0.7))
        fcirc_alpha(screen, (40, 200, 220, 18), bx+bx_off, by+by_off, br)
    # Bubble dots
    rng2 = random.Random(55)
    for i in range(30):
        bub_x = rng2.randint(10, W-10)
        bub_y = rng2.randint(10, GH-10)
        bub_x += int(8 * math.sin(t * 0.5 + i * 0.4))
        bub_r = rng2.randint(1, 3)
        bub_a = int(40 + 20 * math.sin(t * 1.2 + i))
        fcirc_alpha(screen, (150, 230, 255, bub_a), bub_x, bub_y, bub_r)
    # Scanlines
    scan = pygame.Surface((W, GH), pygame.SRCALPHA)
    for sy in range(0, GH, 8):
        pygame.draw.line(scan, (0, 0, 0, 12), (0, sy), (W, sy))
    screen.blit(scan, (0, 0))
    pygame.draw.rect(screen, (20, 80, 140), (0, 0, W, GH), 2)


def draw_bg_neon(screen, static_surfs, t):
    screen.fill((8, 6, 16))
    vp_x, vp_y = W // 2, GH // 3
    # Perspective grid lines (12 lines, 8 horizontals)
    grid_col = (30, 60, 90)
    for i in range(12):
        edge_x = int(i * W / 11)
        pygame.draw.line(screen, grid_col, (vp_x, vp_y), (edge_x, GH), 1)
    for j in range(8):
        hy = vp_y + int((GH - vp_y) * (j + 1) / 8)
        pygame.draw.line(screen, grid_col, (0, hy), (W, hy), 1)
    # Neon edge glow
    pygame.draw.rect(screen, (0, 220, 255), (0, 0, W, GH), 2)
    pygame.draw.rect(screen, (0, 160, 200), (2, 2, W-4, GH-4), 1)
    # Animated scan stripes
    for i in range(3):
        stripe_y = int((t * 80 + i * (GH // 3)) % GH)
        stripe_surf = pygame.Surface((W, 3), pygame.SRCALPHA)
        pygame.draw.rect(stripe_surf, (0, 180, 255, 25), (0, 0, W, 3))
        screen.blit(stripe_surf, (0, stripe_y))
    # Neon dots
    rng = random.Random(99)
    for i in range(6):
        ndx = rng.randint(80, W-80)
        ndy = rng.randint(40, GH-40)
        nd_col = (0, 220, 255) if i % 2 == 0 else (255, 60, 180)
        nd_a = int(150 + 80 * math.sin(t * 2.5 + i * 1.2))
        fcirc_alpha(screen, (*nd_col, nd_a), ndx, ndy, 4)


def draw_background(screen, style, static_surfs, t):
    if style == "space":
        draw_bg_space(screen, static_surfs, t)
    elif style == "deep_ocean":
        draw_bg_ocean(screen, static_surfs, t)
    elif style == "neon_city":
        draw_bg_neon(screen, static_surfs, t)
    else:
        draw_bg_grid(screen)


def make_head_surf(character):
    """Pre-render a character head surface (CELL×CELL) facing RIGHT."""
    s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
    draw_head(s, 0, 0, RIGHT, character)
    return s


def draw_menu(screen, fonts, save, food_surfs, body_surfs, character, static_surfs=None):
    font_big, font_med, font_small = fonts
    s = T[save["language"]]
    draw_background(screen, save.get("bg_style", "grid"), static_surfs or {}, pygame.time.get_ticks()/1000.0)
    draw_centered(screen, font_big, "MAMMOTH", 80, TITLE_C)

    # Character selection cards
    char_names = {"mammoth": s["char_mammoth"], "bunny": s["char_bunny"], "bear": s["char_bear"]}
    centers_x = [W//4, W//2, W*3//4]
    card_w, card_h = 240, 240
    rects = {}

    mx, my = pygame.mouse.get_pos()
    t = pygame.time.get_ticks() / 1000.0
    char_sparkle_colors = {"mammoth": ACCENT, "bunny": PINK, "bear": HONEY_C}

    for i, char in enumerate(CHARACTERS):
        cx = centers_x[i]
        card_x = cx - card_w // 2
        card_y = 220 - card_h // 2

        is_selected = (character == char)
        is_hovered = pygame.Rect(card_x, card_y, card_w, card_h).collidepoint(mx, my)

        # Eased hover
        if is_hovered:
            _hover_t[char] = min(1.0, _hover_t.get(char, 0.0) + 0.12)
        else:
            _hover_t[char] = max(0.0, _hover_t.get(char, 0.0) - 0.12)
        lift = int(8 * ease_in_out_quad(_hover_t[char]))
        ry = card_y - lift

        # Drop shadow
        shadow_surf = pygame.Surface((card_w + 8, card_h + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 70),
                         (0, 0, card_w + 8, card_h + 12), border_radius=14)
        screen.blit(shadow_surf, (card_x - 2, ry + 10))

        # Pulsing glow around selected card
        if is_selected:
            pulse = 0.5 + 0.5 * math.sin(t * 3)
            glow_alpha = int(55 + 45 * pulse)
            glow_pad = int(6 + 3 * pulse)
            glow_surf = pygame.Surface((card_w + glow_pad * 2, card_h + glow_pad * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*ACCENT, glow_alpha),
                             (0, 0, card_w + glow_pad * 2, card_h + glow_pad * 2), border_radius=16)
            screen.blit(glow_surf, (card_x - glow_pad, ry - glow_pad))

        # Card background with hover state
        bg_color = BTN_SEL if is_selected else (BTN_HOV if is_hovered else BTN_BG)
        border_color = ACCENT if is_selected else (TEXT_C if is_hovered else GRID_C)
        pygame.draw.rect(screen, bg_color, (card_x, ry, card_w, card_h), border_radius=12)

        # Gradient highlight (light shimmer at top of card)
        grad_surf = pygame.Surface((card_w, card_h // 2), pygame.SRCALPHA)
        for gy in range(card_h // 2):
            ga = int(22 * (1.0 - gy / (card_h / 2)))
            pygame.draw.line(grad_surf, (255, 255, 255, ga), (0, gy), (card_w, gy))
        screen.blit(grad_surf, (card_x, ry))

        pygame.draw.rect(screen, border_color, (card_x, ry, card_w, card_h), 4, border_radius=12)

        # Draw body
        screen.blit(body_surfs[char], (cx - CELL//2, ry + 30))
        # Draw food
        screen.blit(food_surfs[char], (cx - CELL//2, ry + 100))
        # Draw name
        name_lbl = font_small.render(char_names[char], True, TEXT_C)
        screen.blit(name_lbl, name_lbl.get_rect(center=(cx, ry + 200)))

        # Character-coloured sparkles
        random.seed(42 + i * 7)
        sparkle_c = char_sparkle_colors[char]
        for sp_i in range(5):
            sp_x = cx + random.randint(-card_w // 2 - 15, card_w // 2 + 15)
            sp_y = ry + random.randint(-10, card_h + 10)
            sp_size = random.randint(1, 2)
            sp_alpha = int(70 * abs(math.sin(t * 1.5 + sp_i + i * 1.3)))
            sp_surf = pygame.Surface((sp_size * 2 + 1, sp_size * 2 + 1), pygame.SRCALPHA)
            pygame.draw.circle(sp_surf, (*sparkle_c, sp_alpha), (sp_size, sp_size), sp_size)
            screen.blit(sp_surf, (sp_x - sp_size, sp_y - sp_size))

        # Store original card_y rect for click detection (unaffected by hover float)
        rects[f"char_{char}"] = pygame.Rect(card_x, card_y, card_w, card_h)

    # Control buttons
    rects["play"] = make_rect(W//2, 540)
    rects["settings"] = make_rect(W//2, 618)
    rects["quit"] = make_rect(W//2, 696)

    draw_btn(screen, font_med, s["play"], rects["play"])
    draw_btn(screen, font_med, s["settings_btn"], rects["settings"])
    draw_btn(screen, font_med, s["quit"], rects["quit"])

    return rects


def draw_mode_select(screen, fonts, save):
    font_big, font_med, font_small = fonts
    s = T[save["language"]]
    draw_background(screen, save.get("bg_style", "grid"), {}, pygame.time.get_ticks()/1000.0)
    draw_centered(screen, font_big, s["mode_select"], 80, TITLE_C)

    modes = [
        ("classic",    s["mode_classic"],    s["mode_classic_d"]),
        ("timeattack", s["mode_timeattack"], s["mode_timeattack_d"]),
        ("zen",        s["mode_zen"],        s["mode_zen_d"]),
        ("obstacles",  s["mode_obstacles"],  s["mode_obstacles_d"]),
    ]
    # Adjusted y positions for 1024×828 screen
    ys = [240, 340, 440, 540]
    rects = {}
    for (mode_key, mode_name, mode_desc), y in zip(modes, ys):
        r = make_rect(W//2, y, 420, 60)
        draw_btn(screen, font_med, mode_name, r, selected=(save.get("last_mode") == mode_key))
        desc = font_small.render(mode_desc, True, ACCENT_DIM)
        screen.blit(desc, desc.get_rect(center=(W//2, y+46)))
        rects[mode_key] = r

    rects["back"] = make_rect(W//2, 680)
    draw_btn(screen, font_med, s["back"], rects["back"])
    return rects


def draw_settings(screen, fonts, save):
    font_big, font_med, font_small = fonts
    lang = save["language"]
    s = T[lang]
    draw_background(screen, save.get("bg_style", "grid"), {}, pygame.time.get_ticks()/1000.0)
    draw_centered(screen, font_big, s["settings_btn"], 80, TITLE_C)

    rects = {}
    LABEL_R = 300
    C2 = [560, 700]
    C3 = [460, 600, 740]
    C4 = [360, 480, 600, 720]

    def row(y, label_key, specs, small=False):
        lbl = font_med.render(s[label_key], True, TEXT_C)
        screen.blit(lbl, lbl.get_rect(midright=(LABEL_R, y)))
        if len(specs) == 4:
            centers = C4
            bw = 90
        elif len(specs) == 3:
            centers = C3
            bw = 105
        else:
            centers = C2
            bw = 120
        f  = font_small if small else font_med
        for i, (key, text, sel) in enumerate(specs):
            r = make_rect(centers[i], y, bw, 50)
            draw_btn(screen, f, text, r, selected=sel)
            rects[key] = r

    # Adjusted y positions for 1024×828 screen
    row(270, "language_label", [("lang_de","DE", lang=="de"), ("lang_en","EN", lang=="en")])
    row(355, "speed_label",    [("speed_slow", s["slow"],   save["speed"]=="slow"),
                                 ("speed_normal", s["normal"], save["speed"]=="normal"),
                                 ("speed_fast", s["fast"],   save["speed"]=="fast")], small=True)
    row(440, "grid_label",     [("grid_on",  s["on"],  save["show_grid"]),
                                 ("grid_off", s["off"], not save["show_grid"])])
    row(525, "sound_label",    [("sound_on", s["on"],  save["sound"]),
                                 ("sound_off",s["off"], not save["sound"])])
    row(610, "bg_style_label", [
        ("bg_grid",  s["bg_grid"],  save.get("bg_style","grid")=="grid"),
        ("bg_space", s["bg_space"], save.get("bg_style","grid")=="space"),
        ("bg_ocean", s["bg_ocean"], save.get("bg_style","grid")=="deep_ocean"),
        ("bg_neon",  s["bg_neon"],  save.get("bg_style","grid")=="neon_city"),
    ], small=True)

    rects["back"] = make_rect(W//2, 750)
    draw_btn(screen, font_med, s["back"], rects["back"])
    return rects


def build_static_surfs():
    """Pre-compute surfaces that never change between frames."""
    # Checker (blue-tinted)
    checker = pygame.Surface((W, GH), pygame.SRCALPHA)
    for x in range(COLS):
        for y in range(ROWS):
            if (x + y) % 2 == 0:
                pygame.draw.rect(checker, (15, 22, 45, 10),
                                 (x*CELL, y*CELL, CELL, CELL))

    vignette = pygame.Surface((W, GH), pygame.SRCALPHA)
    for y in range(GH):
        alpha = int(50 * max(0, 1.0 - min(y / 80, (GH - y) / 80)))
        pygame.draw.line(vignette, (0, 0, 0, alpha), (0, y), (W, y))

    # Stars background for space style
    stars_bg = pygame.Surface((W, H), pygame.SRCALPHA)
    rng = random.Random(42)
    for _ in range(80):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H)
        sr = rng.randint(1, 2)
        sc = rng.choice([(255,255,255), (200,220,255), (180,200,255)])
        sa = rng.randint(100, 220)
        pygame.draw.circle(stars_bg, (*sc, sa), (sx, sy), sr)

    # Nebula for space style
    nebula_bg = pygame.Surface((W, H), pygame.SRCALPHA)
    rng2 = random.Random(88)
    for _ in range(20):
        nx = rng2.randint(100, W-100)
        ny = rng2.randint(80, H-80)
        nr = rng2.randint(60, 130)
        pygame.draw.ellipse(nebula_bg, (80, 40, 120, 4),
                            (nx-nr, ny-nr//2, nr*2, nr))

    # Ocean background gradient
    ocean_bg = pygame.Surface((W, H))
    for y in range(H):
        t = y / H
        r = int(5 + 10*t)
        g = int(20 + 30*t)
        b = int(45 + 40*t)
        pygame.draw.line(ocean_bg, (r, g, b), (0, y), (W, y))

    return {
        "checker": checker,
        "vignette": vignette,
        "stars_bg": stars_bg,
        "nebula_bg": nebula_bg,
        "ocean_bg": ocean_bg,
    }


def draw_snake_body(screen, snake, character, prev_snake=None, move_t=1.0):
    """Draw the snake body as one continuous tube (circles + polygon connectors)."""
    if len(snake) < 2:
        return

    body_colors = {
        "mammoth": (MB, MF, (210, 168, 100)),
        "bunny":   (BUNNY_BODY, (215, 210, 210), (240, 238, 238)),
        "bear":    (BEAR_BODY, BEAR_LIGHT, (225, 185, 130)),
    }
    col_outer, col_mid, col_inner = body_colors.get(character, body_colors["mammoth"])
    R  = int(CELL * 0.40)
    R2 = int(CELL * 0.26)
    R3 = int(CELL * 0.13)

    def interp_center(i):
        if prev_snake and move_t < 1.0 and i < len(prev_snake):
            bx = prev_snake[i][0] + (snake[i][0] - prev_snake[i][0]) * move_t
            by = prev_snake[i][1] + (snake[i][1] - prev_snake[i][1]) * move_t
        else:
            bx, by = float(snake[i][0]), float(snake[i][1])
        return int(bx * CELL + CELL // 2), int(by * CELL + CELL // 2)

    n = len(snake)
    centers = [interp_center(i) for i in range(n)]

    # Filled polygon connectors between consecutive segment centers
    for i in range(len(centers) - 1):
        ax, ay = centers[i]
        bx, by = centers[i + 1]
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length < 1:
            continue
        nx = -dy / length * R
        ny =  dx / length * R
        pts = [
            (int(ax + nx), int(ay + ny)),
            (int(ax - nx), int(ay - ny)),
            (int(bx - nx), int(by - ny)),
            (int(bx + nx), int(by + ny)),
        ]
        pygame.draw.polygon(screen, col_outer, pts)
        # Mid polygon
        nx2 = -dy / length * R2
        ny2 =  dx / length * R2
        pts2 = [
            (int(ax + nx2), int(ay + ny2)),
            (int(ax - nx2), int(ay - ny2)),
            (int(bx - nx2), int(by - ny2)),
            (int(bx + nx2), int(by + ny2)),
        ]
        pygame.draw.polygon(screen, col_mid, pts2)

    # Circle caps at each body segment (index 1 = neck to end = tail)
    for i, (cx_c, cy_c) in enumerate(centers[1:], 1):
        seg_i = i  # segment index (0=head)
        # Tail taper: last 3 segments shrink
        tail_idx = n - 1 - (i - 1)  # distance from tail = 0 for last
        if tail_idx < 3:
            taper = max(0.55, 1.0 - (3 - tail_idx - 1) * 0.15)
        else:
            taper = 1.0
        r_o = max(4, int(R * taper))
        r_m = max(2, int(R2 * taper))
        r_i = max(1, int(R3 * taper))
        fcirc(screen, col_outer, cx_c, cy_c, r_o)
        fcirc(screen, col_mid,   cx_c, cy_c, r_m)
        # Inner specular (top-left offset)
        fcirc(screen, col_inner, cx_c - 2, cy_c - 2, r_i)


def draw_game_scene(screen, fonts, save, snake, direction, food, score,
                    character, mode, time_left, obstacles, food_surfs, body_surfs, particles,
                    prev_snake=None, move_t=1.0, static_surfs=None, t=0.0):
    font_big, font_med, font_small = fonts
    bg_style = save.get("bg_style", "grid")
    t_val = pygame.time.get_ticks() / 1000.0
    draw_background(screen, bg_style, static_surfs or {}, t_val)

    # Noise pattern overlay (subtle per-frame randomness)
    noise = pygame.Surface((W, GH), pygame.SRCALPHA)
    for _ in range(200):
        nx = random.randint(0, W-1)
        ny = random.randint(0, GH-1)
        noise_alpha = random.randint(5, 15)
        pygame.draw.line(noise, (50, 50, 50, noise_alpha), (nx, ny), (nx+1, ny+1), 1)
    screen.blit(noise, (0, 0))

    if save["show_grid"]:
        draw_grid(screen)

    # Checkerboard (pre-computed)
    if static_surfs:
        screen.blit(static_surfs["checker"], (0, 0))
    else:
        checker = pygame.Surface((W, GH), pygame.SRCALPHA)
        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(checker, (15, 22, 45, 10),
                                     (x*CELL, y*CELL, CELL, CELL))
        screen.blit(checker, (0, 0))

    if mode == "obstacles":
        for obs in obstacles:
            pygame.draw.rect(screen, OBSTACLE_C,
                             (obs[0]*CELL+3, obs[1]*CELL+3, CELL-6, CELL-6), border_radius=6)
    draw_snake_body(screen, snake, character, prev_snake, move_t)
    if snake:
        # Interpolate head position
        if prev_snake and move_t < 1.0:
            hx = prev_snake[0][0] + (snake[0][0] - prev_snake[0][0]) * move_t
            hy = prev_snake[0][1] + (snake[0][1] - prev_snake[0][1]) * move_t
            head_px = int(hx * CELL)
            head_py = int(hy * CELL)
        else:
            head_px = snake[0][0] * CELL
            head_py = snake[0][1] * CELL
        draw_head(screen, head_px, head_py, direction, character)
    screen.blit(food_surfs[character], (food[0]*CELL, food[1]*CELL))
    draw_particles(screen, particles)

    # Vignette (pre-computed)
    if static_surfs:
        screen.blit(static_surfs["vignette"], (0, 0))
    else:
        vignette = pygame.Surface((W, GH), pygame.SRCALPHA)
        for y in range(GH):
            alpha = int(50 * max(0, 1.0 - min(y / 80, (GH - y) / 80)))
            pygame.draw.line(vignette, (0, 0, 0, alpha), (0, y), (W, y))
        screen.blit(vignette, (0, 0))

    # Border around gameplay area
    pygame.draw.rect(screen, ACCENT_DIM, (0, 0, W, GH), 3)

    draw_hud(screen, font_small, save, score, character, mode, time_left)


# ── Transitions ───────────────────────────────────────────────────────────────

class Transition:
    def __init__(self):
        self.alpha = 0
        self.dir = 0
        self.target = None
        self.raw_t = 0.0

    def begin(self, target):
        self.raw_t = 0.0
        self.alpha = 0
        self.dir = 1
        self.target = target

    def update(self):
        if self.dir != 0:
            self.raw_t = max(0.0, min(1.0, self.raw_t + self.dir * 0.047))
            self.alpha = int(255 * smoothstep(self.raw_t))
            if self.raw_t >= 1.0 and self.dir == 1:
                self.dir = -1
                return self.target
            elif self.raw_t <= 0.0 and self.dir == -1:
                self.dir = 0
        return None

    def draw(self, screen):
        if self.dir != 0 or self.alpha > 0:
            ov = pygame.Surface((W, H))
            ov.set_alpha(self.alpha)
            ov.fill((0, 0, 0))
            screen.blit(ov, (0, 0))


# ── Font helpers ──────────────────────────────────────────────────────────────

def _best_font(size, bold=False):
    for name in ("SF Pro Display", "Helvetica Neue", "Arial"):
        f = pygame.font.SysFont(name, size, bold=bold)
        if f:
            return f
    return pygame.font.Font(None, size)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mammoth")
    clock = pygame.time.Clock()

    font_big   = _best_font(64, bold=True)
    font_med   = _best_font(34)
    font_small = _best_font(23)
    fonts = (font_big, font_med, font_small)

    sounds      = init_sounds()
    save        = load_save()
    food_surfs  = {c: make_food_surf(c) for c in CHARACTERS}
    body_surfs  = {c: make_body_surf(c) for c in CHARACTERS}
    static_surfs = build_static_surfs()

    character = save.get("last_character", "mammoth")
    mode      = save.get("last_mode", "classic")

    snake, direction, food, score, obstacles = new_game(mode)
    pending_dir = direction
    particles   = []
    state       = "menu"
    time_left   = float(TIME_ATTACK_SECS)
    last_tick   = pygame.time.get_ticks()
    last_logic_ms = 0

    # Smooth movement variables
    prev_snake = []
    move_t = 1.0

    # Transition system
    transition = Transition()

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                write_save(save)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == "playing":
                    state = "paused"
                    play_snd(sounds, "pause", save)
                elif state == "paused":
                    transition.begin("menu")
                    write_save(save)
                elif state == "dead":
                    transition.begin("menu")
                    write_save(save)
                elif state in ("settings", "mode_select"):
                    transition.begin("menu")
                elif state == "menu":
                    write_save(save)
                    pygame.quit()
                    sys.exit()

        # ── Menu (integrated character selection) ────────────────────────
        if state == "menu":
            btn = draw_menu(screen, fonts, save, food_surfs, body_surfs, character, static_surfs)
            for event in events:
                # Character card clicks
                for char in CHARACTERS:
                    if was_clicked(btn.get(f"char_{char}", pygame.Rect(0,0,0,0)), event):
                        play_snd(sounds, "click", save)
                        character = char
                        save["last_character"] = char
                if was_clicked(btn.get("play", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save)
                    transition.begin("mode_select")
                elif was_clicked(btn.get("settings", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save)
                    transition.begin("settings")
                elif was_clicked(btn.get("quit", pygame.Rect(0,0,0,0)), event):
                    write_save(save)
                    pygame.quit()
                    sys.exit()

        # ── Mode select ────────────────────────────────────────────────────
        elif state == "mode_select":
            btn = draw_mode_select(screen, fonts, save)
            for event in events:
                for m in ["classic", "timeattack", "zen", "obstacles"]:
                    if was_clicked(btn.get(m, pygame.Rect(0,0,0,0)), event):
                        play_snd(sounds, "click", save)
                        mode = m
                        save["last_mode"] = m
                        snake, direction, food, score, obstacles = new_game(mode)
                        pending_dir = direction
                        particles   = []
                        time_left   = float(TIME_ATTACK_SECS)
                        last_logic_ms = pygame.time.get_ticks()
                        prev_snake = []
                        move_t = 1.0
                        transition.begin("playing")
                if was_clicked(btn.get("back", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save)
                    transition.begin("menu")

        # ── Settings ──────────────────────────────────────────────────────
        elif state == "settings":
            btn = draw_settings(screen, fonts, save)
            for event in events:
                if was_clicked(btn.get("lang_de", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["language"] = "de"
                elif was_clicked(btn.get("lang_en", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["language"] = "en"
                elif was_clicked(btn.get("speed_slow", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["speed"] = "slow"
                elif was_clicked(btn.get("speed_normal", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["speed"] = "normal"
                elif was_clicked(btn.get("speed_fast", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["speed"] = "fast"
                elif was_clicked(btn.get("grid_on", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["show_grid"] = True
                elif was_clicked(btn.get("grid_off", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["show_grid"] = False
                elif was_clicked(btn.get("sound_on", pygame.Rect(0,0,0,0)), event):
                    save["sound"] = True
                elif was_clicked(btn.get("sound_off", pygame.Rect(0,0,0,0)), event):
                    save["sound"] = False
                elif was_clicked(btn.get("bg_grid", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["bg_style"] = "grid"
                elif was_clicked(btn.get("bg_space", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["bg_style"] = "space"
                elif was_clicked(btn.get("bg_ocean", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["bg_style"] = "deep_ocean"
                elif was_clicked(btn.get("bg_neon", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save); save["bg_style"] = "neon_city"
                elif was_clicked(btn.get("back", pygame.Rect(0,0,0,0)), event):
                    play_snd(sounds, "click", save)
                    write_save(save)
                    transition.begin("menu")

        # ── Paused ────────────────────────────────────────────────────────
        elif state == "paused":
            draw_game_scene(screen, fonts, save, snake, direction, food, score,
                            character, mode, time_left, obstacles, food_surfs, body_surfs, particles,
                            prev_snake, move_t, static_surfs)
            ov = pygame.Surface((W, GH), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 160))
            screen.blit(ov, (0, 0))
            s = T[save["language"]]
            draw_centered(screen, font_big,   s["pause"],      GH//2-30, TITLE_C)
            draw_centered(screen, font_small, s["pause_hint"], GH//2+28)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    play_snd(sounds, "pause", save)
                    state = "playing"
                    last_logic_ms = pygame.time.get_ticks()

        # ── Playing / Dead ────────────────────────────────────────────────
        else:
            s = T[save["language"]]

            if state == "playing":
                # Separate logic tick from render tick
                now_ms = pygame.time.get_ticks()
                logic_interval = 1000 / get_speed(score, save["speed"])
                if now_ms - last_logic_ms >= logic_interval:
                    prev_snake = list(snake)
                    move_t = 0.0

                    # Time attack countdown
                    if mode == "timeattack":
                        time_left -= (now_ms - last_logic_ms) / 1000.0
                        if time_left <= 0:
                            time_left = 0
                            key = hs_key(character, mode)
                            if score > save["high_scores"].get(key, 0):
                                save["high_scores"][key] = score
                                write_save(save)
                            play_snd(sounds, "dead", save)
                            state = "dead"

                    if state == "playing":
                        direction = pending_dir
                        hx, hy = snake[0]
                        dx, dy = direction
                        new_head = (hx+dx, hy+dy)

                        if mode == "zen":
                            new_head = (new_head[0] % COLS, new_head[1] % ROWS)

                        wall_hit = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
                        if wall_hit or new_head in obstacles or new_head in snake:
                            key = hs_key(character, mode)
                            if score > save["high_scores"].get(key, 0):
                                save["high_scores"][key] = score
                                write_save(save)
                            play_snd(sounds, "dead", save)
                            state = "dead"
                        else:
                            snake.insert(0, new_head)
                            if new_head == food:
                                score += 1
                                particles += emit_particles(food, food_color(character))
                                play_snd(sounds, "eat", save)
                                food = random_food(snake, obstacles)
                            else:
                                snake.pop()

                    last_logic_ms = now_ms
                else:
                    # Interpolate between logic ticks
                    raw_t = min(1.0, (now_ms - last_logic_ms) / logic_interval)
                    move_t = ease_out_cubic(raw_t)

            # Input
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if state == "dead":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            play_snd(sounds, "click", save)
                            snake, direction, food, score, obstacles = new_game(mode)
                            pending_dir = direction
                            particles   = []
                            time_left   = float(TIME_ATTACK_SECS)
                            last_logic_ms = pygame.time.get_ticks()
                            prev_snake = []
                            move_t = 1.0
                            state       = "playing"
                    elif state == "playing":
                        if event.key == pygame.K_p:
                            play_snd(sounds, "pause", save)
                            state = "paused"
                        else:
                            nd = {
                                pygame.K_UP: UP,    pygame.K_w: UP,
                                pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                                pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                                pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
                            }.get(event.key)
                            if nd and nd != OPPOSITES[pending_dir]:
                                pending_dir = nd
                                # Force early logic tick for immediate key response
                                _now = pygame.time.get_ticks()
                                _interval = 1000 / get_speed(score, save["speed"])
                                if _now - last_logic_ms >= 60:
                                    last_logic_ms = _now - int(_interval)

            update_particles(particles)
            draw_game_scene(screen, fonts, save, snake, direction, food, score,
                            character, mode, time_left, obstacles, food_surfs, body_surfs, particles,
                            prev_snake, move_t, static_surfs)

            if state == "dead":
                dark_overlay(screen)
                go_txt = s["time_up"] if (mode == "timeattack" and time_left <= 0) else s["game_over"]
                draw_centered(screen, font_big,   go_txt,                    GH//2-65, PINK)
                draw_centered(screen, font_med,   s["score_msg"].format(score), GH//2+10)
                draw_centered(screen, font_small, s["restart_hint"],           GH//2+55)

        # Update transitions
        next_state = transition.update()
        if next_state:
            state = next_state

        # Draw fade transition overlay
        transition.draw(screen)

        pygame.display.flip()
        clock.tick(RENDER_FPS)


if __name__ == "__main__":
    main()
