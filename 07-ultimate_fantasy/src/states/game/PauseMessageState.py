from typing import Callable, Optional
from src.states.game.BattleMessageState import BattleMessageState

class PauseMessageState(BattleMessageState):
    def enter(
        self,
        message: str = "",
        on_close: Optional[Callable[[], None]] = None,
    ) -> None:
        super().enter(
            battle_state=None,
            message=message,
            on_close=on_close,
            can_input=True,
        )