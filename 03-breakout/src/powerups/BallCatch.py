from typing import TypeVar
from src.powerups.PowerUp import PowerUp


class BallCatch(PowerUp):
    """
    Power-up that allows the player to catch the ball again
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)


    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.ball_caught = True
        paddle.time_ball_caught = 8.0
        self.active = False
