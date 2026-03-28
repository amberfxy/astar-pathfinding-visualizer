"""
CS5800 A* Pathfinding Visualizer — Constants & Layout
All magic numbers live here so other modules stay clean.
"""

# ── Window ─────────────────────────────────────────────────────────────────
WIN_W, WIN_H = 1380, 820
FPS          = 60

# ── Grid geometry ──────────────────────────────────────────────────────────
CELL    = 20            # pixels per cell side
GRID_N  = 20            # rows = cols
GRID_PX = GRID_N * CELL # 400 px

# ── Panel layout ───────────────────────────────────────────────────────────
TOOLBAR_H     = 102     # top toolbar height
PANEL_W       = GRID_PX + 20   # 420 — 10 px padding each side
PANEL_MARGIN  = 10
# x origin of each of the 3 panels
PANEL_XS = [PANEL_MARGIN + i * (PANEL_W + PANEL_MARGIN) for i in range(3)]
# [10, 440, 870]

PANEL_LABEL_H = 26      # algorithm name header height
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
C_OPEN     = (100, 149, 237)   # cornflower blue  — open/frontier set
C_CLOSED   = (255, 140,   0)   # dark orange      — expanded / closed set
C_CURRENT  = (255, 215,   0)   # gold             — node being expanded
C_PATH     = (148,   0, 211)   # dark violet      — optimal path
C_START    = ( 50, 205,  50)   # lime green
C_GOAL     = (220,  20,  60)   # crimson

# ── UI palette ─────────────────────────────────────────────────────────────
C_BG        = ( 28,  28,  38)
C_PANEL_BG  = ( 40,  42,  54)
C_TOOLBAR   = ( 20,  20,  32)
C_METRICS   = ( 24,  26,  38)
C_LEGEND    = ( 20,  22,  35)
C_GRID_LINE = ( 95, 100, 120)
C_TEXT      = (225, 225, 225)
C_DIM       = (140, 140, 155)
C_ACCENT    = (  0, 188, 212)   # cyan
C_BORDER    = ( 65,  70, 100)

C_BTN_IDLE   = ( 55,  58,  80)
C_BTN_HOVER  = ( 80,  85, 115)
C_BTN_ACTIVE = ( 0,  150, 136)  # teal
C_BTN_TEXT   = (230, 230, 230)

# ── Algorithm display names & colours ─────────────────────────────────────
ALGO_NAMES  = ['Dijkstra', 'A* — Manhattan', 'A* — Euclidean']
ALGO_COLORS = [(100, 210, 255), (130, 255, 160), (255, 190, 80)]

# ── Animation speeds (ms between ticks) ───────────────────────────────────
SPEEDS      = [('Slow', 300), ('Med', 80), ('Fast', 20), ('Max', 0)]
SPEED_IDX   = 1   # default: Med

# ── Pygame custom event ────────────────────────────────────────────────────
import pygame
ANIM_TICK = pygame.USEREVENT + 1
