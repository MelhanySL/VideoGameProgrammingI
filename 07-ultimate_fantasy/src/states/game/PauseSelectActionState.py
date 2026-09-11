from typing import Any, Callable, Dict, List, Tuple
import pygame
from gale.state import BaseState
from gale.timer import Timer
import settings
from src.gui.Menu import Menu
from src.states.game.PauseSelectTargetState import PauseSelectTargetState

class PauseSelectActionState(BaseState):
    def enter(
        self, caster: Any, panels: List[Any], on_cancel: Callable[[], None]
    ) -> None:
        self.caster = caster
        self.panels = panels
        self.on_cancel = on_cancel

        items = []
        self.disabled_indices = []

        for action_index, action in enumerate(caster.actions):
            if self.caster.dead or action["target_type"] == "enemy":
                items.append((action["name"], lambda: None))
                self.disabled_indices.append(action_index)
            else:
                items.append((action["name"], self._make_selector(action)))
                
        items.append(("Cancel", self._cancel))

        caster_panel = next(panel_obj for panel_obj, character_obj, _, _ in self.panels if character_obj == self.caster)
        
        menu_width = 110
        menu_height = 20 + len(items) * 20

        menu_x = 20
        menu_y = caster_panel.y

        self.menu = Menu(menu_x, menu_y, menu_width, menu_height, items=items, font=settings.FONTS["small"])

        while self.menu.list_view.selected_index in self.disabled_indices:
            self.menu.list_view.on_navigate((0, 1))

    def _make_selector(self, action: Dict[str, Any]) -> Callable[[], None]:
        return lambda: self._select_action(action)

    def _select_action(self, action: Dict[str, Any]) -> None:
        if action["require_target"]:
            self.state_machine.push(
                PauseSelectTargetState(self.state_machine),
                panels=self.panels,
                on_target_selected=lambda target: self._resolve(action, target),
                on_cancel=lambda: None,
            )
        else:
            self.state_machine.pop()
            alive_targets = [character_obj for panel_obj, character_obj, hp_bar, exp_bar in self.panels if not character_obj.dead]
            amount = action["func"](self.caster, alive_targets, action.get("strength"))
            settings.SOUNDS[action["sound_effect"]].play()

            for panel_obj, character_obj, hp_bar, exp_bar in self.panels:
                if not character_obj.dead:
                    Timer.tween(0.5, [(hp_bar, {"value": character_obj.current_hp})])

            self._show_result(f"{action['name']} for {amount} HP to each target.")

    def _resolve(self, action: Dict[str, Any], target: Any) -> None:
        self.state_machine.pop()
        amount = action["func"](self.caster, target, action.get("strength"))
        settings.SOUNDS[action["sound_effect"]].play()
        
        for panel_obj, character_obj, hp_bar, exp_bar in self.panels:
            if character_obj == target:
                Timer.tween(0.5, [(hp_bar, {"value": target.current_hp})])
                break

        self._show_result(f"{action['name']} for {amount} HP to {target.name}.")

    def _show_result(self, message: str) -> None:
        from src.states.game.PauseMessageState import PauseMessageState
        self.state_machine.push(
            PauseMessageState(self.state_machine),
            message=message,
            on_close=self.on_cancel
        )

    def _cancel(self) -> None:
        self.state_machine.pop()
        self.on_cancel()

    def _navigate(self, direction: Tuple[int, int]) -> None:
        old_index = self.menu.list_view.selected_index
        total_items = len(self.menu.list_view.items)

        for _ in range(total_items):
            if self.menu.list_view.on_navigate(direction):
                if self.menu.list_view.selected_index not in self.disabled_indices:
                    settings.SOUNDS["blip"].stop()
                    settings.SOUNDS["blip"].play()
                    return
        self.menu.list_view.selected_index = old_index

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "move_up":
            self._navigate((0, -1))
        elif input_id == "move_down":
            self._navigate((0, 1))
        elif input_id == "enter":
            self.menu.confirm()
        elif input_id == "quit" or input_id == "pause":
            self._cancel()

    def render(self, surface: pygame.Surface) -> None:
        self.menu.render(surface)

        for disabled_index in self.disabled_indices:
            row_rect = self.menu.list_view.row_rect(disabled_index)
            overlay = pygame.Surface((row_rect.width, row_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, row_rect)
