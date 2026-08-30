from typing import TypeVar
from src.powerups.PowerUp import PowerUp


class ShieldPower(PowerUp):
    """
    Power-up to add a protective barrier at the bottom edge of the screen 
    that acts as a last line of defense to prevent a ball loss
    """
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 2)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.shield_active = True
        self.active = False
