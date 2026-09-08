"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameObject.
"""

from typing import Any, Dict
from gale.animation import Animation

import pygame

import settings


class GameObject:
    def __init__(self, definition: Dict[str, Any], x: float, y: float) -> None:
        self.type = definition["type"]
        self.texture_id = definition["texture"]
        self.frame_index = definition.get("frame", 1)

        # Whether it acts as an obstacle or not.
        self.solid = definition["solid"]

        self.default_state = definition["default_state"]
        self.state = self.default_state
        self.states = definition["states"]

        self.x = x
        self.y = y
        self.width = definition["width"]
        self.height = definition["height"]

        self.on_collide = definition.get("on_collide") or (lambda: None)

        # Whether this object is consumable or not.
        self.consumable = definition.get("consumable", False)
        self.on_consume = definition.get("on_consume") or (lambda player, obj: None)

        # An object could be taken or not.
        self.takeable = definition.get("takeable", False)
        self.taken = False

        self.interactable = definition.get("interactable", False)
        self.interacted = False

        self._create_animations(definition)

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        if self.current_animation is None:
            return

        self.current_animation.update(dt)
        
        if self.current_animation.times_played > 0:
            self.current_animation.times_played = 0
            self.current_animation = None
            self.state = "open"

    def _create_animations(self, definition: Dict[str, Any]) -> Dict[str, Animation]:
        self.animations = {}

        for name, definition in definition.get("animations", {}).items():
            self.animations[name] = Animation(
                definition["frames"],
                definition.get("interval", 0),
                loops=definition.get("loops"),
            )

        self.current_animation = None    

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        if self.current_animation:
            frame_index = self.current_animation.get_current_frame()
        else:
            frame_index = self.states[self.state].get("frame", self.frame_index)
        surface.blit(
            settings.TEXTURES[self.texture_id],
            (self.x + offset_x, self.y + offset_y),
            settings.frame(self.texture_id, frame_index),
        )
