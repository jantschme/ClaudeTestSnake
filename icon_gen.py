#!/usr/bin/env python3
"""
Generate Mammoth app icon from draw_head_mammoth() rendering.
Creates 1024px PNG, then resizes to all .icns sizes (1024, 512, 256, 128, 64, 32, 16).
"""

import pygame
import pygame.gfxdraw
import math
import subprocess
import sys
from pathlib import Path

# ── Colors (from snake.py) ─────────────────────────────────────────────────────
MB         = (112,  74,  36)
MD         = ( 78,  50,  20)
MF         = (162, 118,  64)
TUSK_C     = (252, 246, 200)
SKIN_C     = ( 92,  58,  24)
EYE_W      = (242, 230, 210)
EYE_P      = ( 15,  10,   4)

BG_WHITE   = (255, 255, 255)

# ── Drawing primitives ─────────────────────────────────────────────────────────

def fcirc(surf, color, cx, cy, r):
    cx, cy, r = int(cx), int(cy), int(r)
    if r <= 0:
        return
    pygame.gfxdraw.filled_circle(surf, cx, cy, r, color)
    pygame.gfxdraw.aacircle(surf, cx, cy, r, color)


def fur_strokes(surf, ox, oy, seed, count=16):
    import random
    rng = random.Random(seed)
    c = 44  # CELL size (not used for icon, just for compatibility)
    for _ in range(count):
        fx = rng.randint(ox + 4, ox + c - 7)
        fy = rng.randint(oy + 4, oy + c - 7)
        a  = rng.uniform(-1.4, 1.4)
        ln = rng.randint(5, 11)
        ex = max(ox + 2, min(ox + c - 3, fx + int(math.cos(a) * ln)))
        ey = max(oy + 2, min(oy + c - 3, fy + int(math.sin(a) * ln)))
        pygame.draw.line(surf, MF, (fx, fy), (ex, ey), 2)


def draw_head_mammoth_icon(screen, cx, cy, scale=1):
    """
    Render Mammoth head centered at (cx, cy) with given scale.
    Adapted from snake.py draw_head_mammoth() for icon rendering.
    """
    c = int(44 * scale)  # base cell size
    direction = (0, -1)  # pointing up
    dx, dy = direction
    px2, py2 = -dy, dx  # perp = (1, 0)

    # Main head rect
    r = c // 4
    pygame.draw.rect(screen, MB, (cx - c//2 + 2, cy - c//2 + 2, c-4, c-4), border_radius=r)
    pygame.draw.rect(screen, MD, (cx - c//2 + c//3, cy - c//2 + c//3, c*2//3-4, c*2//3-4), border_radius=r//2)
    fur_strokes(screen, cx - c//2, cy - c//2, seed=11, count=12)

    # Ear
    ear_cx = int(cx - dx*c//4 + px2*c//3)
    ear_cy = int(cy - dy*c//4 + py2*c//3)
    pygame.draw.ellipse(screen, MB, (ear_cx-c//6, ear_cy-c//6, c//3, c//3))
    pygame.draw.ellipse(screen, SKIN_C, (ear_cx-c//10, ear_cy-c//10, c//5, c//5))

    # Eye
    ecx = int(cx + dx*c//5 - px2*c//6)
    ecy = int(cy + dy*c//5 - py2*c//6)
    fcirc(screen, EYE_W, ecx, ecy, c//8)
    fcirc(screen, EYE_P, ecx+dx+1, ecy+dy+1, c//13)
    fcirc(screen, (255,255,255), ecx+2, ecy-2, max(1, c//22))

    # Tusks (2x, left/right)
    for sign in (1, -1):
        sx = cx + dx*c//3 + sign*px2*c//8
        sy = cy + dy*c//3 + sign*py2*c//8
        pts = []
        for i in range(10):
            t = i / 9.0
            pts.append((int(sx + dx*t*c*0.65 + sign*px2*t*c*0.50),
                         int(sy + dy*t*c*0.65 + sign*py2*t*c*0.50)))
        pygame.draw.lines(screen, TUSK_C, False, pts, 4)
        pygame.draw.lines(screen, (236,224,170), False, pts, 2)
        fcirc(screen, (240,232,180), pts[-1][0], pts[-1][1], 3)

    # Trunk
    trunk_pts = []
    for i in range(9):
        t = i / 8.0
        wobble = math.sin(t * math.pi * 1.6) * c * 0.13 * (1 - t*0.6)
        trunk_pts.append((int(cx + dx*(c//2 + t*c*0.58) + px2*wobble),
                           int(cy + dy*(c//2 + t*c*0.58) + py2*wobble)))
    pygame.draw.lines(screen, SKIN_C, False, trunk_pts, max(4, c//8))
    fcirc(screen, (75,45,18),  trunk_pts[-1][0],   trunk_pts[-1][1],   c//10)
    fcirc(screen, (105,66,28), trunk_pts[-1][0]-1, trunk_pts[-1][1]-1, c//15)


def generate_icon(size=1024):
    """Generate icon PNG of given size."""
    pygame.init()

    # Create surface
    surf = pygame.Surface((size, size))
    surf.fill(BG_WHITE)

    # Render Mammoth head centered
    scale = size / 256  # base on 256px nominal
    draw_head_mammoth_icon(surf, size//2, size//2, scale)

    return surf


def main():
    print("🎨 Generating Mammoth icon...")

    # Generate 1024px icon
    icon_1024 = generate_icon(1024)
    pygame.image.save(icon_1024, "icon_1024.png")
    print("✅ Generated icon_1024.png")

    # Create .iconset directory
    iconset_dir = Path("Mammoth.iconset")
    iconset_dir.mkdir(exist_ok=True)
    print(f"📁 Created {iconset_dir}/")

    # Generate resized versions for .icns
    sizes = [512, 256, 128, 64, 32, 16]
    for size in sizes:
        icon = generate_icon(size)
        filename = f"Mammoth.iconset/icon_{size}x{size}.png"
        pygame.image.save(icon, filename)
        print(f"   → {filename}")

    # Also create 2x variants (macOS retina)
    sizes_2x = [256, 128, 64, 32, 16]
    for size in sizes_2x:
        icon = generate_icon(size * 2)
        filename = f"Mammoth.iconset/icon_{size}x{size}@2x.png"
        pygame.image.save(icon, filename)
        print(f"   → {filename}")

    # Convert .iconset to .icns using iconutil
    print("\n🔄 Converting to .icns...")
    try:
        result = subprocess.run(
            ["iconutil", "-c", "icns", "Mammoth.iconset", "-o", "Mammoth.icns"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Generated Mammoth.icns")
        else:
            print(f"❌ iconutil failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ iconutil not found. Install via: xcode-select --install")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    # Clean up .iconset
    import shutil
    shutil.rmtree(iconset_dir, ignore_errors=True)
    print(f"🧹 Removed {iconset_dir}/")

    pygame.quit()
    print("\n✨ Icon generation complete!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
