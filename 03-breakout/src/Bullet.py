import pygame
import settings

from typing import Any

class Bullet:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.texture = settings.TEXTURES["shot"]
        self.vy = -150
        self.size = 8
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float) -> None:
        self.y += self.vy * dt

        if self.y < -self.size:
            self.active = False
    
    def render(self, surface):
        surface.blit(self.texture, (self.x, self.y))