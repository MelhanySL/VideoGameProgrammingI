"""
ISPPV1 2023
Study Case: Ultimate Fantasy (RPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PauseMenuState: pushed on top of PlayState
(which keeps rendering, frozen, underneath it) when the player presses
the pause key. Offers Continue/Save/Load another/Quit -- the canonical
"menu over a paused game" use case StateStack was introduced for back in
Chapter 8. Loading another save or quitting first warns (via
ConfirmState) if the current game has progress since its last save (see
World.dirty), and proceeds however the player answers.
"""

from typing import Any, NamedTuple

import pygame

from gale.save import SaveError, SaveManager
from gale.state import BaseState
from gale.ui.progress_bar import ProgressBar

import settings
from src.gui.Menu import Menu
from src.gui.Panel import Panel
from src.gui.theme import BAR_THEME

from src.states.game.PauseSelectTargetState import PauseSelectTargetState
from src.states.game.PauseSelectActionState import PauseSelectActionState

class CharacterPanel(NamedTuple):
    panel: Panel
    character: Any
    hp_bar: ProgressBar
    exp_bar: ProgressBar


UNSAVED_LOAD_WARNING = (
    "You have unsaved progress. Do you want to save the current game before loading another?"
)
UNSAVED_QUIT_WARNING = (
    "You have unsaved progress. Do you want to save the current game before quitting?"
)


class PauseMenuState(BaseState):
    def enter(self, play_state: Any) -> None:
        self.play_state = play_state

        self.menu = Menu(
            10,
            settings.VIRTUAL_HEIGHT / 2 - 60,
            130,
            120,
            items=[
                ("Continue", self.close),
                ("Actions", self._actions),
                ("Save game", self._save),
                ("Load another game", self._load_another),
                ("Quit", self._quit),
            ],
            font=settings.FONTS["small"],
        )

        self.panels = []
        start_x = 145
        start_y = 20
        width = 115
        height = 85
        padding_x = 5
        padding_y = 10

        idx = 0
        for char_id in sorted(self.play_state.world.party.characters.keys()):
            character = self.play_state.world.party.characters[char_id]
            row = idx // 2
            col = idx % 2
            px = start_x + col * (width + padding_x)
            py = start_y + row * (height + padding_y)
            panel = Panel(px, py, width, height)

            hp_bar = ProgressBar(
                px + 5,
                py + 37,
                width - 10,
                4,
                value=character.current_hp,
                max_value=character.hp,
                color=pygame.Color(189, 32, 32),
                theme=BAR_THEME,
            )

            exp_bar = ProgressBar(
                px + 5,
                py + 69,
                width - 10,
                4,
                value=character.current_exp,
                max_value=character.exp_to_level,
                color=pygame.Color(32, 32, 189),
                theme=BAR_THEME,
            )

            self.panels.append(CharacterPanel(panel, character, hp_bar, exp_bar))
            idx += 1

    def close(self) -> None:
        self.state_machine.pop()

    def _actions(self) -> None:
        def on_character_selected(character: Any) -> None:
            self.state_machine.push(
                PauseSelectActionState(self.state_machine),
                caster=character,
                panels=self.panels,
                on_cancel=lambda: None
            )

        self.state_machine.push(
            PauseSelectTargetState(self.state_machine),
            panels=self.panels,
            on_target_selected=on_character_selected,
            on_cancel=lambda: None
        )

    # -- save --------------------------------------------------------------

    def _save(self) -> None:
        from src.states.game.SlotSelectState import SlotSelectState

        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="save",
            on_select=self._do_save,
            on_close=self._cancel_slot_select,
        )

    def _cancel_slot_select(self) -> None:
        self.state_machine.pop()

    def _do_save(self, slot: str) -> None:
        from src.states.game.ShowTextState import ShowTextState

        self.play_state.save_game(slot)
        self.state_machine.pop()  # SlotSelectState
        self.state_machine.pop()  # this PauseMenuState
        self.state_machine.push(
            ShowTextState(self.state_machine),
            color=(255, 255, 255),
            text="Game saved",
            on_complete=lambda: None,
        )

    # -- load another --------------------------------------------------------

    def _load_another(self) -> None:
        if self.play_state.world.dirty:
            from src.states.game.ConfirmState import ConfirmState

            self.state_machine.push(
                ConfirmState(self.state_machine),
                message=UNSAVED_LOAD_WARNING,
                on_yes=self._save_before_loading,
                on_no=self._show_load_slots,
            )
        else:
            self._show_load_slots()

    def _save_before_loading(self) -> None:
        from src.states.game.SlotSelectState import SlotSelectState

        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="save",
            on_select=self._do_save_before_loading,
            on_close=self._cancel_slot_select,
        )

    def _do_save_before_loading(self, slot: str) -> None:
        self.play_state.save_game(slot)
        self.state_machine.pop()  # SlotSelectState
        self._show_load_slots()

    def _show_load_slots(self) -> None:
        from src.states.game.SlotSelectState import SlotSelectState

        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="load",
            on_select=self._do_load,
            on_close=self._cancel_slot_select,
        )

    def _do_load(self, slot: str) -> None:
        from src.states.game.FadeInState import FadeInState
        from src.states.game.PlayState import PlayState

        try:
            save_data = SaveManager().load(slot)
        except SaveError:
            # Corrupted/unreadable: leave the paused game exactly as it was.
            return

        party_genders = {int(k): v for k, v in save_data["party"]["genders"].items()}

        def on_complete() -> None:
            # Whatever the discarded game's own region music was --
            # World.__init__ (for the fresh PlayState below) only ever
            # expects to be following StartState's "intro", not another
            # already-playing World, so it never stops these on its own.
            settings.stop_music("town")
            settings.stop_music("world")

            self.state_machine.pop()  # SlotSelectState
            self.state_machine.pop()  # this PauseMenuState
            self.state_machine.pop()  # the old, now-discarded PlayState
            self.state_machine.push(
                PlayState(self.state_machine),
                party_genders=party_genders,
                save_data=save_data,
            )

        self.state_machine.push(
            FadeInState(self.state_machine),
            color=(0, 0, 0),
            time=1,
            on_complete=on_complete,
        )

    # -- quit ----------------------------------------------------------------

    def _quit(self) -> None:
        if self.play_state.world.dirty:
            from src.states.game.ConfirmState import ConfirmState

            self.state_machine.push(
                ConfirmState(self.state_machine),
                message=UNSAVED_QUIT_WARNING,
                on_yes=self._save_before_quitting,
                on_no=self._do_quit,
            )
        else:
            self._do_quit()

    def _save_before_quitting(self) -> None:
        from src.states.game.SlotSelectState import SlotSelectState

        self.state_machine.push(
            SlotSelectState(self.state_machine),
            mode="save",
            on_select=self._do_save_before_quitting,
            on_close=self._cancel_slot_select,
        )

    def _do_save_before_quitting(self, slot: str) -> None:
        self.play_state.save_game(slot)
        self._do_quit()

    def _do_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    # -- BaseState -------------------------------------------------------

    def update(self, dt: float) -> None:
        self.menu.update(dt)

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if input_id == "move_up":
            self.menu.navigate((0, -1))
        elif input_id == "move_down":
            self.menu.navigate((0, 1))
        elif input_id == "enter":
            self.menu.confirm()

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        x: float,
        y: float,
        color=(255, 255, 255),
    ) -> None:
        font = settings.FONTS["small"]
        shadow = font.render(text, True, (0, 0, 0))
        surface.blit(shadow, (x + 1, y + 1))
        surf = font.render(text, True, color)
        surface.blit(surf, (x, y))

    def render(self, surface: pygame.Surface) -> None:
        self.menu.render(surface)

        for panel, character, hp_bar, exp_bar in self.panels:
            panel.render(surface)

            if character.current_animation is not None:
                surface.blit(
                    settings.TEXTURES[character.texture],
                    (panel.x + 5, panel.y + 5),
                    character.current_animation.get_current_frame(),
                )

            self._draw_text(surface, character.name, panel.x + 70, panel.y + 5)
            
            if character.dead:
                self._draw_text(surface, "DEATH", panel.x + 75, panel.y + 20, (255, 50, 50))

            self._draw_text(surface, f"Nivel: {character.level}", panel.x + 25, panel.y + 10)
            self._draw_text(surface, f"HP: {int(character.current_hp)}/{int(character.hp)}", panel.x + 5, panel.y + 27)
            hp_bar.render(surface)

            self._draw_text(surface, f"MP: {int(character.magic)}", panel.x + 5, panel.y + 45)
            self._draw_text(surface, f"EXP: {int(character.current_exp)}/{int(character.exp_to_level)}", panel.x + 5, panel.y + 59)
            exp_bar.render(surface)
        