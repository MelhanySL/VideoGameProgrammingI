"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings

from src.Tile import Tile
from src.powerups import LineClear, ColorBomb

class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.highlighted_i1 = -1
        self.highlighted_j1 = -1

        self.is_dragging = False
        self.dragged_tile = None
        
        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:

        if self.dragged_tile: 
            pos_x, pos_y = pygame.mouse.get_pos()

            virtual_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            virtual_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            self.dragged_tile.x = virtual_x - self.board.x - (settings.TILE_SIZE // 2)
            self.dragged_tile.y = virtual_y - self.board.y - (settings.TILE_SIZE // 2)

            self.dragged_tile.drag_x = virtual_x - (settings.TILE_SIZE // 2)
            self.dragged_tile.drag_y = virtual_y - (settings.TILE_SIZE // 2)

        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active or input_id != "click":
            return

        pos_x, pos_y = input_data.position
        pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
        pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

        i = (pos_y - self.board.y) // settings.TILE_SIZE
        j = (pos_x - self.board.x) // settings.TILE_SIZE

        if input_data.pressed:
            self._handle_click_pressed(i, j)
        else:
            self._handle_drag(i, j)

    def _handle_click_pressed(self, i: int, j: int) -> None:
        if not (0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH):
            return
        
        tile = self.board.tiles[i][j]

        if tile is not None:
            if tile.is_powerup:
                self.active = False
                affected_tiles = tile.activate(self.board)
                
                self.board.matches.append(list(affected_tiles))
                self._calculate_matches([])
                return

            self.is_dragging = True
            self.highlighted_i1 = i
            self.highlighted_j1 = j
            self.dragged_tile = self.board.tiles[i][j]
            self.dragged_tile.dragging = True

    def _handle_drag(self, i:int, j:int) -> None:
        self.is_dragging = False
        tile1 = self.dragged_tile

        if not tile1:
            return

        tile1.dragging = False
        self.dragged_tile = None
        
        di = abs(i - self.highlighted_i1)
        dj = abs(j - self.highlighted_j1)

        if di <= 1 and dj <= 1 and di != dj and 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH and self.board.tiles[i][j] is not None:
            self.active = False
            tile2 = self.board.tiles[i][j]
            self._evaluate_matches(tile1, tile2, i, j)
            
        elif tile1:
            self._revert_animation(tile1)

        
    def _revert_animation(self, tile: Tile) -> None:
        Timer.tween(0.25, [(tile, {"x": tile.j * settings.TILE_SIZE, "y": tile.i * settings.TILE_SIZE})])
        
    def _swap_tiles(self, tile1: Tile, tile2: Tile) -> None:
        (
            self.board.tiles[tile1.i][tile1.j],
            self.board.tiles[tile2.i][tile2.j],
        ) = (
            self.board.tiles[tile2.i][tile2.j],
            self.board.tiles[tile1.i][tile1.j],
        )
        tile1.i, tile1.j, tile2.i, tile2.j = (
            tile2.i, 
            tile2.j, 
            tile1.i, 
            tile1.j
        )

    def _evaluate_matches(self, tile1: Tile, tile2: Tile, i: int, j: int) -> None:
        def arrive():
            self._swap_tiles(tile1, tile2)
            matches = self.board.calculate_matches_for([tile1, tile2])

            if matches is None:
                self._swap_tiles(tile1, tile2)
                settings.SOUNDS["error"].play()

                def reset_turn():
                    self.active = True

                Timer.tween(
                    0.25,
                    [
                        (tile1, {"x": tile1.j * settings.TILE_SIZE, "y": tile1.i * settings.TILE_SIZE}),
                        (tile2, {"x": tile2.j * settings.TILE_SIZE, "y": tile2.i * settings.TILE_SIZE}),
                    ],
                    on_finish=reset_turn,
                )
            else:
                self.board.matches = []
                self._calculate_matches([tile1, tile2], original_tiles=[tile1, tile2])

        Timer.tween(
            0.25,
            [
                (tile1, {"x": j * settings.TILE_SIZE, "y": i * settings.TILE_SIZE}),
                (tile2, {"x": self.highlighted_j1 * settings.TILE_SIZE, "y": self.highlighted_i1 * settings.TILE_SIZE}),
            ],
            on_finish=arrive,
        )
    
    def _calculate_matches(self, tiles: List, original_tiles: List[Tile] = None) -> None:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            while not self.board.matches_possible():
                self.board._initialize_tiles()

            self.active = True
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        extra_tiles = set()
        for match in matches:
            for tile in match:
                if tile.is_powerup:
                    extra_tiles.update(tile.activate(self.board))

        if extra_tiles:
            matches.append(list(extra_tiles))

        for match in matches:
            self.score += len(match) * 50

            if len(match) >= 4 and original_tiles:
                for tile in match:
                    if tile in original_tiles:
                        if len(match) == 4:
                            power_up = LineClear(tile.i, tile.j, tile.color, tile.variety)
                        else:
                            power_up = ColorBomb(tile.i, tile.j, tile.color, tile.variety)
                        self.board.tiles[tile.i][tile.j] = power_up
                        match.remove(tile)
                        break

        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
