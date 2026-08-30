"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World

from src.modes import NormalMode, HardMode

class TitleScreenState(BaseState):
    def enter(self) -> None:
        self.world = World()
        self.selected = 1

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 4,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        
        render_text(
            surface,
            "Select a mode:",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 4,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

        color = (0, 128, 0) if self.selected == 1 else (255, 255, 255)
        render_text(
            surface,
            "Normal Mode",
            settings.FONTS["medium"],
            (settings.VIRTUAL_WIDTH - 200) / 2,
            2.5 * settings.VIRTUAL_HEIGHT / 4,
            color,
            center=True,
            shadowed=True,
        )

        color = (255, 0, 0) if self.selected == 2 else (255, 255, 255)
        render_text(
            surface,
            "Hard Mode",
            settings.FONTS["medium"],
            (settings.VIRTUAL_WIDTH + 200) / 2,
            2.5 * settings.VIRTUAL_HEIGHT / 4,
            color,
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "Press Enter to start",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            3 * settings.VIRTUAL_HEIGHT / 4,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:

        if input_id == "right" and input_data.pressed and self.selected == 1:
            settings.SOUNDS["select"].play().set_volume(200)
            self.selected = 2
        elif input_id == "left" and input_data.pressed and self.selected == 2:
            settings.SOUNDS["select"].play().set_volume(200)
            self.selected = 1
        elif input_id == "confirm" and input_data.pressed:
            settings.SOUNDS["confirm"].play().set_volume(200)

            game_mode = NormalMode() if self.selected == 1 else HardMode()
            self.state_machine.change("count_down", game_mode)
