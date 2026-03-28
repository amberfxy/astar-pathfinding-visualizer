"""
CS5800 Final Project — Phase 1
Interactive A* Pathfinding Visualizer

Three side-by-side panels visualise Dijkstra, A* (Manhattan), and
A* (Euclidean) expanding nodes step-by-step on the same weighted grid.

Controls
────────
  Mouse drag     — paint selected terrain brush
  Right-click    — erase to empty
  R              — run all algorithms
  Space          — play / pause animation
  →              — step forward one expansion
  C              — clear grid
  H              — toggle f(n) overlay on cells
  Q / Esc        — quit

Authors: Jiaxin Jia · Xiaoyuan Lu · Xinyuan Fan
Course : CS5800 — Algorithms
"""
from __future__ import annotations

import math
import sys
import pygame

from constants import (
    WIN_W, WIN_H, FPS, CELL, GRID_N, GRID_PX,
    PANEL_W, PANEL_MARGIN, PANEL_XS, PANEL_LABEL_H,
    TOOLBAR_H, GRID_Y, METRICS_Y, METRICS_H, LEGEND_Y, LEGEND_H,
    TERRAIN_COLOR, TERRAIN_LABEL,
    C_BG, C_PANEL_BG, C_TOOLBAR, C_METRICS, C_LEGEND,
    C_GRID_LINE, C_TEXT, C_DIM, C_ACCENT, C_BORDER,
    C_BTN_IDLE, C_BTN_HOVER, C_BTN_ACTIVE, C_BTN_TEXT,
    C_OPEN, C_CLOSED, C_CURRENT, C_PATH, C_START, C_GOAL,
    ALGO_NAMES, ALGO_COLORS, SPEEDS, SPEED_IDX, ANIM_TICK,
)
from grid import Grid
from algorithms import AlgState, dijkstra_gen, astar_manhattan_gen, astar_euclidean_gen
from logger import log_run


# ══════════════════════════════════════════════════════════════════════════════
# Button widget
# ══════════════════════════════════════════════════════════════════════════════

class Button:
    def __init__(
        self,
        rect: tuple[int, int, int, int],
        label: str,
        swatch: tuple[int, int, int] | None = None,
    ) -> None:
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.swatch  = swatch      # optional coloured square on left
        self.active  = False
        self.hovered = False

    def update_hover(self, pos: tuple[int, int]) -> None:
        self.hovered = self.rect.collidepoint(pos)

    def hit(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def draw(self, surf: pygame.Surface, font: pygame.font.Font) -> None:
        bg = C_BTN_ACTIVE if self.active else (C_BTN_HOVER if self.hovered else C_BTN_IDLE)
        pygame.draw.rect(surf, bg,       self.rect, border_radius=5)
        pygame.draw.rect(surf, C_BORDER, self.rect, 1, border_radius=5)

        x_off = 6
        if self.swatch is not None:
            sr = pygame.Rect(self.rect.x + 5, self.rect.centery - 6, 12, 12)
            pygame.draw.rect(surf, self.swatch, sr, border_radius=2)
            pygame.draw.rect(surf, (160, 160, 160), sr, 1, border_radius=2)
            x_off = 22

        lbl = font.render(self.label, True, C_BTN_TEXT)
        surf.blit(lbl, (self.rect.x + x_off,
                        self.rect.centery - lbl.get_height() // 2))


# ══════════════════════════════════════════════════════════════════════════════
# App
# ══════════════════════════════════════════════════════════════════════════════

class App:

    # ── Brushes available in toolbar ──────────────────────────────────────
    BRUSHES = [
        ('wall',  'Wall',   TERRAIN_COLOR['wall']),
        ('empty', 'Empty',  TERRAIN_COLOR['empty']),
        ('grass', 'Grass',  TERRAIN_COLOR['grass']),
        ('swamp', 'Swamp',  TERRAIN_COLOR['swamp']),
        ('start', 'Start',  C_START),
        ('goal',  'Goal',   C_GOAL),
        ('predict', 'Predict Path', (255, 105, 180)), # Hot Pink for prediction
    ]

    # Layer 1: The Trap constraints
    MAX_WALLS = 5

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(
            'CS5800  ·  A* Pathfinding Visualizer  ·  Phase 1'
        )
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock  = pygame.time.Clock()

        # ── Fonts ──────────────────────────────────────────────────────────
        self.f_cell    = pygame.font.SysFont('monospace',  8)   # f(n) in cells
        self.f_small   = pygame.font.SysFont('sans',      11)
        self.f_btn     = pygame.font.SysFont('sans',      12)
        self.f_label   = pygame.font.SysFont('sans',      13, bold=True)
        self.f_metrics = pygame.font.SysFont('monospace', 12)
        self.f_title   = pygame.font.SysFont('sans',      14, bold=True)

        # ── State ──────────────────────────────────────────────────────────
        self.grid      = Grid()
        self.brush     = 'wall'
        self.painting  = False
        self.last_cell: tuple[int, int] | None = None   # avoid redundant repaints
        self.show_vals = True

        self.predicted_path: list[tuple[int, int]] = []
        self.wall_count = 0  # Number of walls placed by the player
        
        # ── Algorithm generators & latest states ───────────────────────────
        self.gens:   list                          = [None, None, None]
        self.states: list[AlgState | None]         = [None, None, None]
        self.done:   list[bool]                    = [False, False, False]

        # ── Animation ──────────────────────────────────────────────────────
        self.speed_idx  = SPEED_IDX
        self.animating  = False
        self._logged    = False
        self.global_time = 0.0

        # ── Toolbar buttons ────────────────────────────────────────────────
        self._build_toolbar()

    # ── Toolbar construction ───────────────────────────────────────────────

    def _build_toolbar(self) -> None:
        ROW1_Y = 8
        ROW2_Y = 54
        H = 36

        # ── Row 1: Brush buttons ───────────────────────────────────────────
        self.brush_btns: list[Button] = []
        x = 10
        for terrain, label, color in self.BRUSHES:
            btn_w = 100 if terrain == 'predict' else 78
            btn = Button((x, ROW1_Y, btn_w, H), label, swatch=color)
            btn.active  = (terrain == self.brush)
            btn.terrain = terrain          # type: ignore[attr-defined]
            self.brush_btns.append(btn)
            x += btn_w + 4

        # ── Row 1 right: preset maps ───────────────────────────────────────
        self.preset_btns: list[Button] = []
        px = 640  # Moved further right to avoid overlapping with Predict Path
        for label, key in [('Maze', 'maze'), ('Barrier', 'barrier'), ('Random', 'random')]:
            btn = Button((px, ROW1_Y, 75, H), label)
            btn.key = key      # type: ignore[attr-defined]
            self.preset_btns.append(btn)
            px += 80

        # ── Row 2: Action & speed buttons ─────────────────────────────────
        self.action_btns: dict[str, Button] = {}
        ax = 10
        for key, label, w in [
            ('run',   'Run ▶ (R)',   100),
            ('play',  '⏸ Pause',     90),
            ('step+', 'Step → (→)',  90),
            ('reset', 'Reset',       68),
            ('clear', 'Clear',       64),
        ]:
            btn = Button((ax, ROW2_Y, w, H), label)
            self.action_btns[key] = btn
            ax += w + 7

        # ── Row 2 right: speed + toggle ────────────────────────────────────
        self.speed_btns: list[Button] = []
        sx = 520
        for i, (name, _) in enumerate(SPEEDS):
            btn = Button((sx, ROW2_Y, 58, H), name)
            btn.active = (i == self.speed_idx)
            self.speed_btns.append(btn)
            sx += 63

        self.action_btns['vals'] = Button((sx + 5, ROW2_Y, 82, H), 'f(n) vals')
        self.action_btns['vals'].active = self.show_vals

    # ── Main loop ──────────────────────────────────────────────────────────

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # Calculate delta time in seconds
            self.global_time += dt              # Update global time for shaders

            self._handle_events()
            self._draw()

    # ── Event handling ─────────────────────────────────────────────────────

    def _handle_events(self) -> None:
        mp = pygame.mouse.get_pos()
        all_btns = (self.brush_btns + self.preset_btns
                    + list(self.action_btns.values()) + self.speed_btns)
        for btn in all_btns:
            btn.update_hover(mp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            elif event.type == pygame.KEYDOWN:
                self._on_key(event.key)

            elif event.type == ANIM_TICK:
                self._tick()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.painting = True
                    self.last_cell = None
                    self._on_click(mp)
                elif event.button == 3:
                    # Right-click = erase
                    self.painting = True
                    self.last_cell = None
                    self._paint_at(mp, erase=True)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.painting = False
                self.last_cell = None

            elif event.type == pygame.MOUSEMOTION and self.painting:
                erase = pygame.mouse.get_pressed()[2]
                self._paint_at(mp, erase=bool(erase))

    def _on_key(self, key: int) -> None:
        if key == pygame.K_r:
            self._do_run()
        elif key == pygame.K_SPACE:
            self._do_play_pause()
        elif key == pygame.K_RIGHT:
            self._do_step(+1)
        elif key == pygame.K_c:
            self._do_clear()
        elif key == pygame.K_h:
            self._toggle_vals()
        elif key in (pygame.K_q, pygame.K_ESCAPE):
            self._quit()

    def _on_click(self, pos: tuple[int, int]) -> None:
        # Brush buttons
        for btn in self.brush_btns:
            if btn.hit(pos):
                self.brush = btn.terrain       # type: ignore[attr-defined]
                for b in self.brush_btns:
                    b.active = (b.terrain == self.brush)  # type: ignore[attr-defined]
                return

        # Preset buttons
        for btn in self.preset_btns:
            if btn.hit(pos):
                self._load_preset(btn.key)    # type: ignore[attr-defined]
                return

        # Action buttons
        for key, btn in self.action_btns.items():
            if btn.hit(pos):
                {
                    'run':   self._do_run,
                    'play':  self._do_play_pause,
                    'step+': lambda: self._do_step(+1),
                    'reset': self._do_reset,
                    'clear': self._do_clear,
                    'vals':  self._toggle_vals,
                }[key]()
                return

        # Speed buttons
        for i, btn in enumerate(self.speed_btns):
            if btn.hit(pos):
                self._set_speed(i)
                return

        # Grid click → paint
        self._paint_at(pos)

    # ── Painting ───────────────────────────────────────────────────────────

    def _paint_at(self, pos: tuple[int, int], erase: bool = False) -> None:
        """Convert screen coordinates to grid cell and apply brush."""
        for px in PANEL_XS:
            gx = pos[0] - (px + 10)
            gy = pos[1] - GRID_Y
            if 0 <= gx < GRID_PX and 0 <= gy < GRID_PX:
                col = gx // CELL
                row = gy // CELL
                if (row, col) == self.last_cell:
                    return
                self.last_cell = (row, col)

                if erase:
                    if self.brush == 'predict':
                        if (row, col) in self.predicted_path:
                            self.predicted_path.remove((row, col))
                    else:
                        if self.grid.get_terrain(row, col) == 'wall':
                            self.wall_count = max(0, self.wall_count - 1)
                        self.grid.set_terrain(row, col, 'empty')
                elif self.brush == 'start':
                    self.grid.move_start(row, col)
                elif self.brush == 'goal':
                    self.grid.move_goal(row, col)
                elif self.brush == 'predict':
                    if (row, col) not in self.predicted_path:
                        self.predicted_path.append((row, col))
                else:
                    if self.brush == 'wall' and self.grid.get_terrain(row, col) != 'wall':
                        if self.wall_count < self.MAX_WALLS:
                            self.grid.set_terrain(row, col, self.brush)
                            self.wall_count += 1
                        else:
                            print("Max walls reached!")
                    elif self.brush != 'wall':
                        if self.grid.get_terrain(row, col) == 'wall':
                            self.wall_count = max(0, self.wall_count - 1)
                        self.grid.set_terrain(row, col, self.brush)

                # Invalidate results when grid changes
                if any(s is not None for s in self.states):
                    self._do_reset()
                return

    # ── Actions ────────────────────────────────────────────────────────────

    def _do_run(self) -> None:
        self._cancel_timer()
        self.gens   = [dijkstra_gen(self.grid),
                       astar_manhattan_gen(self.grid),
                       astar_euclidean_gen(self.grid)]
        self.states = [None, None, None]
        self.done   = [False, False, False]
        self._logged = False
        self._set_timer()
        self.animating = True
        self.action_btns['play'].label = '⏸ Pause'

    def _do_play_pause(self) -> None:
        if all(g is None for g in self.gens):
            self._do_run()
            return
        self.animating = not self.animating
        if self.animating:
            self._set_timer()
            self.action_btns['play'].label = '⏸ Pause'
        else:
            self._cancel_timer()
            self.action_btns['play'].label = '▶ Play'

    def _do_step(self, delta: int) -> None:
        if all(g is None for g in self.gens):
            return
        self._cancel_timer()
        self.animating = False
        self.action_btns['play'].label = '▶ Play'
        if delta > 0:
            self._tick()   # advance all generators one step

    def _do_reset(self) -> None:
        self._cancel_timer()
        self.gens      = [None, None, None]
        self.states    = [None, None, None]
        self.done      = [False, False, False]
        self.animating = False
        self._logged   = False
        self.action_btns['play'].label = '▶ Play'
        self.predicted_path.clear()

    def _do_clear(self) -> None:
        self._do_reset()
        self.grid.clear()
        self.predicted_path.clear()
        self.wall_count = 0

    def _toggle_vals(self) -> None:
        self.show_vals = not self.show_vals
        self.action_btns['vals'].active = self.show_vals

    def _load_preset(self, key: str) -> None:
        self._do_reset()
        {'maze': self.grid.load_maze,
         'barrier': self.grid.load_barrier,
         'random': self.grid.load_random}[key]()

    def _set_speed(self, idx: int) -> None:
        self.speed_idx = idx
        for i, btn in enumerate(self.speed_btns):
            btn.active = (i == idx)
        if self.animating:
            self._cancel_timer()
            self._set_timer()

    def _set_timer(self) -> None:
        ms = SPEEDS[self.speed_idx][1]
        if ms == 0:
            # Max speed — advance as many steps as possible each frame
            pygame.time.set_timer(ANIM_TICK, 16)
        else:
            pygame.time.set_timer(ANIM_TICK, ms)

    def _cancel_timer(self) -> None:
        pygame.time.set_timer(ANIM_TICK, 0)

    # ── Animation tick ─────────────────────────────────────────────────────

    def _tick(self) -> None:
        """Advance all alive generators by one step."""
        all_done = True
        for i, gen in enumerate(self.gens):
            if gen is None or self.done[i]:
                continue
            all_done = False
            try:
                state = next(gen)
                self.states[i] = state
                if state.done:
                    self.done[i] = True
            except StopIteration:
                self.done[i] = True

        # At max speed, keep ticking until all done within the frame
        if SPEEDS[self.speed_idx][1] == 0 and not all_done:
            return   # next ANIM_TICK fires ~16ms later

        if all(self.done):
            if self.animating:
                self._cancel_timer()
                self.animating = False
                self.action_btns['play'].label = '▶ Play'
            # Log results once when all algorithms finish (animation or stepping)
            if not self._logged:
                log_run(ALGO_NAMES, self.states, self.grid)
                self._logged = True

    # ══════════════════════════════════════════════════════════════════════
    # Drawing
    # ══════════════════════════════════════════════════════════════════════

    def _draw(self) -> None:
        self.screen.fill(C_BG)
        self._draw_toolbar()
        for i in range(3):
            self._draw_panel(i)
        self._draw_metrics()
        self._draw_legend()
        pygame.display.flip()

    # ── Toolbar ────────────────────────────────────────────────────────────

    def _draw_toolbar(self) -> None:
        pygame.draw.rect(self.screen, C_TOOLBAR, (0, 0, WIN_W, TOOLBAR_H))
        pygame.draw.line(self.screen, C_BORDER, (0, TOOLBAR_H - 1), (WIN_W, TOOLBAR_H - 1))

        # Title (top-left)
        title = self.f_title.render(
            'A* Pathfinding Visualizer  ·  CS5800', True, C_ACCENT)
        self.screen.blit(title, (WIN_W - title.get_width() - 12, 10))

        # Row 1 label
        lbl = self.f_small.render('Brush:', True, C_DIM)
        self.screen.blit(lbl, (10, 18))

        # Row 2 labels
        lbl2 = self.f_small.render('Controls:', True, C_DIM)
        self.screen.blit(lbl2, (10, 64))

        spd_lbl = self.f_small.render('Speed:', True, C_DIM)
        self.screen.blit(spd_lbl, (520, 64))

        all_btns = (self.brush_btns + self.preset_btns
                    + list(self.action_btns.values()) + self.speed_btns)
        for btn in all_btns:
            btn.draw(self.screen, self.f_btn)

    # ── Panel ──────────────────────────────────────────────────────────────

    def _draw_panel(self, idx: int) -> None:
        px = PANEL_XS[idx]
        py = TOOLBAR_H

        # Panel background
        panel_rect = pygame.Rect(px, py, PANEL_W, LEGEND_Y - py)
        pygame.draw.rect(self.screen, C_PANEL_BG, panel_rect, border_radius=6)
        pygame.draw.rect(self.screen, C_BORDER,   panel_rect, 1, border_radius=6)

        # Algorithm name label
        name_surf = self.f_label.render(ALGO_NAMES[idx], True, ALGO_COLORS[idx])
        self.screen.blit(name_surf, (px + 10, py + 6))

        # Draw grid cells
        self._draw_grid(idx, px + 10, GRID_Y)

        # Footer: per-panel metrics
        self._draw_panel_footer(idx, px, METRICS_Y)

    def _draw_grid(self, idx: int, x0: int, y0: int) -> None:
        state = self.states[idx]
        grid  = self.grid

        path_set: set[tuple] = set(state.path) if (state and state.found) else set()

        for r in range(GRID_N):
            for c in range(GRID_N):
                pos  = (r, c)
                x    = x0 + c * CELL
                y    = y0 + r * CELL
                rect = pygame.Rect(x, y, CELL, CELL)

                # ── Base terrain color ────────────────────────────────────
                if pos == grid.start:
                    color = C_START
                elif pos == grid.goal:
                    color = C_GOAL
                elif state is None:
                    color = grid.base_color(r, c)
                else:
                    color = self._cell_color(state, pos, grid.base_color(r, c), path_set)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, C_GRID_LINE, rect, 1)

                # ── Predicted path overlay ────────────────────────────────
                if pos in self.predicted_path and pos not in (grid.start, grid.goal):
                    # Draw a smaller inner rect to show prediction on top of terrain/state
                    pred_rect = pygame.Rect(x + 4, y + 4, CELL - 8, CELL - 8)
                    pygame.draw.rect(self.screen, (255, 105, 180), pred_rect, border_radius=2)

                # ── f(n) overlay ──────────────────────────────────────────
                if (self.show_vals and state is not None
                        and pos in state.expanded
                        and pos not in (grid.start, grid.goal)):
                    f = state.f_vals.get(pos)
                    if f is not None and f != float('inf'):
                        self._draw_fval(x, y, f)

                # ── Start / Goal labels ───────────────────────────────────
                if pos == grid.start:
                    self._draw_center_label(x, y, 'S')
                elif pos == grid.goal:
                    self._draw_center_label(x, y, 'G')

    def _cell_color(
        self,
        state: AlgState,
        pos: tuple[int, int],
        base: tuple[int, int, int],
        path_set: set,
    ) -> tuple[int, int, int]:
        """Priority: PATH > CURRENT > CLOSED > OPEN > terrain."""
        if pos in path_set:
            from constants import PULSE_SPEED, C_PATH_GLOW
            pulse = (math.sin(self.global_time * PULSE_SPEED) + 1.0) / 2.0
            r = int(C_PATH[0] + (C_PATH_GLOW[0] - C_PATH[0]) * pulse)
            g = int(C_PATH[1] + (C_PATH_GLOW[1] - C_PATH[1]) * pulse)
            b = int(C_PATH[2] + (C_PATH_GLOW[2] - C_PATH[2]) * pulse)
            return (r, g, b)
        if pos == state.current:
            return C_CURRENT
        if pos in state.expanded:
            return C_CLOSED
        if pos in state.open_set:
            return C_OPEN
        return base

    def _draw_fval(self, x: int, y: int, f: float) -> None:
        text = f'{f:.0f}' if f < 1000 else f'{int(f)}'
        surf = self.f_cell.render(text, True, (230, 240, 255))
        # Clip to cell so text never bleeds
        self.screen.set_clip(pygame.Rect(x, y, CELL, CELL))
        self.screen.blit(surf, (x + 1, y + CELL - surf.get_height() - 1))
        self.screen.set_clip(None)

    def _draw_center_label(self, x: int, y: int, char: str) -> None:
        surf = self.f_small.render(char, True, (255, 255, 255))
        self.screen.blit(surf, (x + CELL // 2 - surf.get_width() // 2,
                                y + CELL // 2 - surf.get_height() // 2))

    # ── Per-panel footer metrics ────────────────────────────────────────────

    def _draw_panel_footer(self, idx: int, px: int, fy: int) -> None:
        state = self.states[idx]

        if state is None:
            hint = self.f_small.render('Press R to run', True, C_DIM)
            self.screen.blit(hint, (px + 10, fy + 12))
            return

        lines = [
            f'Expanded : {state.nodes_expanded}',
        ]
        
        # Calculate predicted cost
        predicted_cost = 0.0
        if self.predicted_path:
            for p in self.predicted_path:
                predicted_cost += self.grid.get_cost(p[0], p[1])
                
        if self.predicted_path:
            lines.append(f'Predict Cost: {predicted_cost}')
            
        if state.done:
            if state.found:
                lines.append(f'Path cost: {state.path_cost:.2f}  |  len: {len(state.path)}')
                if self.predicted_path:
                    if abs(predicted_cost - state.path_cost) < 0.001:
                        lines.append(f'Prediction: EXACT MATCH!')
                    else:
                        lines.append(f'Prediction diff: {abs(predicted_cost - state.path_cost)}')
                        
                lines.append(f'Runtime  : {state.runtime_ms:.3f} ms')
                lines.append('Status   : ✓ Path found')
            else:
                lines.append('Status   : ✗ No path exists')
                lines.append(f'Runtime  : {state.runtime_ms:.3f} ms')
        else:
            lines.append('Status   : Searching…')

        for i, line in enumerate(lines):
            color = C_TEXT if i % 2 == 0 else C_DIM
            surf  = self.f_metrics.render(line, True, color)
            self.screen.blit(surf, (px + 10, fy + 4 + i * 16))

    # ── Bottom metrics comparison ───────────────────────────────────────────

    def _draw_metrics(self) -> None:
        rect = pygame.Rect(0, METRICS_Y, WIN_W, METRICS_H)
        pygame.draw.rect(self.screen, C_METRICS, rect)
        pygame.draw.line(self.screen, C_BORDER, (0, METRICS_Y), (WIN_W, METRICS_Y))

        if not any(s is not None and s.done for s in self.states):
            hint = self.f_small.render(
                'Run the algorithms to see a comparison table here.', True, C_DIM)
            self.screen.blit(hint, (20, METRICS_Y + (METRICS_H - hint.get_height()) // 2))
            return

        # Comparison table header
        headers    = ['Algorithm',     'Nodes Expanded', 'Path Cost', 'Path Len', 'Runtime (ms)']
        col_widths = [190,             160,              110,         100,        150]
        tx = 20
        ty = METRICS_Y + 6
        for h, w in zip(headers, col_widths):
            surf = self.f_label.render(h, True, C_ACCENT)
            self.screen.blit(surf, (tx, ty))
            tx += w

        for ri, (state, color) in enumerate(zip(self.states, ALGO_COLORS)):
            if state is None:
                continue
            ty += 17
            tx  = 20
            row = [
                ALGO_NAMES[ri],
                str(state.nodes_expanded) if state.nodes_expanded else '—',
                f'{state.path_cost:.2f}' if state.found else 'N/A',
                str(len(state.path))    if state.found else '—',
                f'{state.runtime_ms:.4f}' if state.done else '…',
            ]
            for i, (val, w) in enumerate(zip(row, col_widths)):
                c    = color if i == 0 else C_TEXT
                surf = self.f_metrics.render(val, True, c)
                self.screen.blit(surf, (tx, ty))
                tx  += w

    # ── Legend row ─────────────────────────────────────────────────────────

    def _draw_legend(self) -> None:
        rect = pygame.Rect(0, LEGEND_Y, WIN_W, LEGEND_H)
        pygame.draw.rect(self.screen, C_LEGEND, rect)
        pygame.draw.line(self.screen, C_BORDER, (0, LEGEND_Y), (WIN_W, LEGEND_Y))

        items: list[tuple[tuple, str]] = [
            (C_START,                  'Start'),
            (C_GOAL,                   'Goal'),
            (C_OPEN,                   'Open set'),
            (C_CLOSED,                 'Expanded'),
            (C_CURRENT,                'Current'),
            (C_PATH,                   'Optimal path'),
            (TERRAIN_COLOR['grass'],   TERRAIN_LABEL['grass']),
            (TERRAIN_COLOR['swamp'],   TERRAIN_LABEL['swamp']),
            (TERRAIN_COLOR['wall'],    TERRAIN_LABEL['wall']),
        ]

        lx = 16
        ly = LEGEND_Y + 10
        for color, label in items:
            pygame.draw.rect(self.screen, color, (lx, ly, 14, 14), border_radius=2)
            pygame.draw.rect(self.screen, (110, 110, 130), (lx, ly, 14, 14), 1, border_radius=2)
            surf = self.f_small.render(label, True, C_DIM)
            self.screen.blit(surf, (lx + 18, ly))
            lx += 18 + surf.get_width() + 18

        # Keyboard shortcuts line
        hints = ('R : Run    Space : Play/Pause    → : Step forward    '
                 'C : Clear    H : Toggle f(n)    Q/Esc : Quit    '
                 'Right-click : Erase')
        hs = self.f_small.render(hints, True, C_DIM)
        self.screen.blit(hs, (16, LEGEND_Y + 30))

        # Step & speed status
        spd_name = SPEEDS[self.speed_idx][0]
        status = (f'Speed : {spd_name}    '
                  f'Algo states : '
                  + '  |  '.join(
                      f'{ALGO_NAMES[i]}: {self.states[i].nodes_expanded if self.states[i] else 0} exp.'
                      for i in range(3)
                  ))
        ss = self.f_small.render(status, True, C_DIM)
        self.screen.blit(ss, (16, LEGEND_Y + 50))

    # ── Utilities ──────────────────────────────────────────────────────────

    @staticmethod
    def _quit() -> None:
        pygame.quit()
        sys.exit()


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    try:
        App().run()
    finally:
        pygame.quit()
