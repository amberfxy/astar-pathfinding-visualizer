"""Constants, colors, and layout for the local Pygame interface."""

# ── Window ─────────────────────────────────────────────────────────────────
WIN_W, WIN_H = 1380, 858
FPS          = 60

# ── Grid geometry ──────────────────────────────────────────────────────────
CELL    = 20            # pixels per cell side
GRID_N  = 20            # rows = cols
GRID_PX = GRID_N * CELL # 400 px

# ── Panel layout ───────────────────────────────────────────────────────────
TOOLBAR_H     = 116     # top toolbar height
PANEL_W       = GRID_PX + 20   # 420 — 10 px padding each side
PANEL_MARGIN  = 10
# x origin of each of the 3 panels
PANEL_XS = [PANEL_MARGIN + i * (PANEL_W + PANEL_MARGIN) for i in range(3)]
# [10, 440, 870]

PANEL_LABEL_H = 22      # algorithm name header height
GRID_Y        = TOOLBAR_H + PANEL_LABEL_H   # y where grid cells start (128)
METRICS_Y     = GRID_Y + GRID_PX            # 528
METRICS_H     = 70
LEGEND_Y      = METRICS_Y + METRICS_H       # 598
LEGEND_H      = WIN_H - LEGEND_Y            # 222

# ── Terrain ────────────────────────────────────────────────────────────────
TERRAIN_COST = {
    'empty': 1,
    'grass': 2,
    'swamp': 5,
    'wall':  float('inf'),
}

TERRAIN_COLOR = {
    'empty': (240, 240, 242),
    'grass': (120, 195,  75),
    'swamp': (130,  90,  40),
    'wall':  ( 38,  38,  48),
}

TERRAIN_LABEL = {
    'empty': 'Empty (cost 1)',
    'grass': 'Grass (cost 2)',
    'swamp': 'Swamp (cost 5)',
    'wall':  'Wall (blocked)',
}

# ── Visualisation colours ──────────────────────────────────────────────────
C_OPEN     = (147, 197, 253)
C_CLOSED   = (254, 215, 170)
C_CURRENT  = (251, 191,  36)
C_PATH     = (124,  58, 237)
C_START    = ( 22, 163,  74)
C_GOAL     = (220,  38,  38)

# ── Neon Path Effect Constants (For Layer 3 & 4) ──────────────────────────
PULSE_SPEED = 4.0
C_PATH_GLOW = (167, 139, 250)

# ── UI palette ─────────────────────────────────────────────────────────────
C_BG          = (248, 250, 252)
C_PANEL_BG    = (255, 255, 255)
C_TOOLBAR_A   = ( 89, 112, 140)
C_TOOLBAR_B   = (138, 164, 188)
C_TOOLBAR_ROW = (240, 244, 255)
C_METRICS     = (238, 242, 255)
C_LEGEND      = (240, 244, 255)
C_GRID_LINE   = (203, 213, 225)
C_TEXT        = ( 30,  58, 138)
C_DIM         = (100, 116, 139)
C_ACCENT      = (217, 119,   6)
C_BORDER      = (191, 219, 254)

C_BTN_IDLE        = (239, 246, 255)
C_BTN_HOVER       = (219, 234, 254)
C_BTN_ACTIVE      = ( 30,  64, 175)
C_BTN_TEXT        = ( 30,  58, 138)
C_BTN_TEXT_ACTIVE = (255, 255, 255)

CLAY_SHADOW    = (30, 64, 175, 46)
CLAY_SHADOW_SM = (30, 64, 175, 30)

# ── Algorithm display names & colours ─────────────────────────────────────
ALGO_NAMES  = ['Dijkstra', 'A* — Manhattan', 'A* — Euclidean']
ALGO_COLORS = [(  2, 132, 199), (  5, 150, 105), (220, 104,   3)]

# ── Animation speeds (ms between ticks) ───────────────────────────────────
SPEEDS      = [('Slow', 300), ('Med', 80), ('Fast', 20), ('Max', 0)]
SPEED_IDX   = 1   # default: Med

# ── Pygame custom event ────────────────────────────────────────────────────
import pygame
ANIM_TICK = pygame.USEREVENT + 1
