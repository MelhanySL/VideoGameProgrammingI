"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World

from src.modes import NormalMode, FlappyGameMode

class PlayingState(BaseState):
    def enter(self, world: Optional[World] = None, mode: Optional[FlappyGameMode] = None, bird: Optional[Bird] = None, score: int = 0) -> None:
        self.world = world if world is not None else World()
        self.world.generate_logs = True
        if bird is not None:
            self.bird = bird
        else:
            self.bird = Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
            )

        self.score = score

        self.mode = mode if mode is not None else NormalMode()

    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.mode.update_world(self.world, dt)
        self.world.update(dt)

        for ghost in self.world.ghosts:
            if not ghost.consumed and ghost.collides(self.bird.get_rect()):
                ghost.consumed = True
                self.bird.ghost()
        touching_ground = self.bird.get_rect().bottom >= settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT

        if self.world.collides(self.bird.get_rect()):
            if touching_ground or not self.bird.ghosting:
                settings.SOUNDS["ghost_music"].stop()
                pygame.mixer.music.unpause()
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["hurt"].play()
                self.state_machine.change("title")
                return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change("pause_state", world=self.world, bird=self.bird, score=self.score, mode=self.mode)

            if self.bird.ghosting:
                settings.SOUNDS["ghost_music"].stop()
                pygame.mixer.music.unpause()
        
        self.mode.on_input(self.bird, input_id, input_data)
