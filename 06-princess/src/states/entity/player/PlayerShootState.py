from typing import TypeVar

import pygame

from gale.state import StateMachine

import settings
from src.states.entity.BaseEntityState import BaseEntityState


class PlayerShootState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon

        self.entity.offset_y = 5
        self.entity.offset_x = 8

        direction = self.entity.direction

        self.entity.change_animation(f"bow-{direction}")

    def enter(self) -> None:
        settings.SOUNDS["shoot-arrow"].stop()
        settings.SOUNDS["shoot-arrow"].play()

        self.entity.current_animation.reset()

    def update(self, dt: float) -> None:

        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
