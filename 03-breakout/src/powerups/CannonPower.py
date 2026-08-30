from typing import TypeVar
from src.powerups.PowerUp import PowerUp


class CannonPower(PowerUp):
    """
    Power-up to add cannons to the paddle's edges that fire simultaneous vertical projectiles 
    with the F key to destroy bricks, allowing only one pair active on screen at a time
    """
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 6)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.cannon_active = True
        paddle.cannon_time = 10.0
        self.active = False
