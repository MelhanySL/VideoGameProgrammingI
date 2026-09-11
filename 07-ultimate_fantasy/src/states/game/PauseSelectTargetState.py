from typing import Any, Callable, List
import pygame
from gale.state import BaseState
import settings

class PauseSelectTargetState(BaseState):
    def enter(
        self,
        panels: List[Any],
        on_target_selected: Callable[[Any], None],
        on_cancel: Callable[[], None],
    ) -> None:
        self.panels = panels
        self.on_target_selected = on_target_selected
        self.on_cancel = on_cancel

        self.current_selection = 0
        for panel_index, (panel, target, hp_bar, exp_bar) in enumerate(self.panels):
            if not target.dead:
                self.current_selection = panel_index
                break

    def _next_alive(self) -> None:
        total_panels = len(self.panels)
        for step_count in range(1, total_panels + 1):
            next_index = (self.current_selection + step_count) % total_panels
            if not self.panels[next_index][1].dead:
                self.current_selection = next_index
                return

    def _prev_alive(self) -> None:
        total_panels = len(self.panels)
        for step_count in range(1, total_panels + 1):
            prev_index = (self.current_selection - step_count) % total_panels
            if not self.panels[prev_index][1].dead:
                self.current_selection = prev_index
                return

    def update(self, dt: float) -> None:
        pass

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "move_left" or input_id == "move_up":
            self._prev_alive()
        elif input_id == "move_right" or input_id == "move_down":
            self._next_alive()
        elif input_id == "enter":
            target = self.panels[self.current_selection][1]
            self.state_machine.pop()
            self.on_target_selected(target)
        elif input_id == "quit" or input_id == "pause":
            self.state_machine.pop()
            self.on_cancel()

    def render(self, surface: pygame.Surface) -> None:
        panel = self.panels[self.current_selection][0]
        surface.blit(
            settings.TEXTURES["cursor-right"],
            (panel.x - 12, panel.y + panel.height / 2 - 8),
        )