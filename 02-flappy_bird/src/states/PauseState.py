import pygame
import settings

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

from src.Bird import Bird
from src.World import World

from src.modes import FlappyGameMode

class PauseState(BaseState):
    def enter(self, world: World, bird: Bird, score: int, mode: FlappyGameMode) -> None:
        self.world = world
        self.bird = bird
        self.score = score
        self.mode = mode

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            "Pause",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

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
            self.state_machine.change("playing", world=self.world, bird=self.bird, score=self.score, mode=self.mode)
            if self.bird.ghosting:
                pygame.mixer.music.pause()
                settings.SOUNDS["ghost_music"].play()
                
    