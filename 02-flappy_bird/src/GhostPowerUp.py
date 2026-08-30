import pygame
import settings

class GhostPowerUp:
    def __init__(self, x: float, y: float, width: float = settings.GHOST_WIDTH, height: float = settings.GHOST_HEIGHT) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.consumed: bool = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.x -= settings.MAIN_SCROLL_SPEED * dt

    def is_out_of_game(self) -> bool:
        return self.x < -self.width or self.consumed

    def render(self, surface: pygame.Surface) -> None:
        if not self.consumed:
            surface.blit(settings.TEXTURES["ghost"], self.get_rect())

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)