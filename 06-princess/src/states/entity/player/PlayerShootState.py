from typing import TypeVar

import pygame

from gale.state import StateMachine

import settings
from src.states.entity.BaseEntityState import BaseEntityState
from src.Bow import Bow
from src.GameObject import GameObject
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Projectile import Projectile


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

        self.arrow = GAME_OBJECT_DEFS["arrow"]
        x = self.entity.x
        y = self.entity.y

        if self.entity.direction == "left":
            x -= 8
        elif self.entity.direction == "right":
            x += self.entity.width
        elif self.entity.direction == "up":
            y -= 8
        elif self.entity.direction == "down":
            y += self.entity.height

        arrow_obj = GameObject(self.arrow, x, y)
        arrow_obj.state = self.entity.direction
        projectile_arrow = Projectile(arrow_obj, self.entity.direction)
        self.dungeon.current_room.projectiles.append(projectile_arrow)


    def update(self, dt: float) -> None:
        
        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
