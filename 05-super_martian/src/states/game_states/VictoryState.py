import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings

class VictoryState(BaseState):
    def enter(self, player) -> None:
        self.player = player
        pygame.mixer.music.stop()
        pygame.mixer.music.load(
            settings.BASE_DIR / "assets" / "sounds" / "victory.mp3"
        )
        pygame.mixer.music.play(loops=-1)


    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("play")

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 130, 196))

        render_text(
            surface,
            "VICTORY!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 40,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "You won! Congratulations",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 - 20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            f"Final Score: {self.player.score}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 10,
            (255, 255, 255),
            shadowed=True,
            center=True,
        )

        render_text(
            surface,
            "Press Enter to play again",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2 + 30,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )