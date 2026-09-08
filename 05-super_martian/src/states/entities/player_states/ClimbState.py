import settings
from src.states.entities.BaseEntityState import BaseEntityState

class ClimbState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation("climb")
        self.entity.vx = 0
        self.entity.vy = 0

    def update(self, dt: float) -> None:
        self.entity.vy = settings.PLAYER_SPEED * self.entity.move_y_direction
        self.entity.vx = settings.PLAYER_SPEED * self.entity.move_direction

        if self.entity.jump_requested:
            self.entity.jump_requested = False
            self.entity.change_state("jump")
            return

        if not self.entity.is_on_ladder():
            if self.entity.on_ground:
                self.entity.change_state("idle")
            else:
                self.entity.change_state("fall")
            return