from src.states.entity.BaseEntityState import BaseEntityState
import random

class BossHurtState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation(f"hurt-{self.entity.direction}")
        self.timer = 0
        
    def process_ai(self, room, dt: float) -> None:
        self.timer += dt
        if self.timer >= 0.6:
            if random.randint(1, 10) <= 3:
                self.entity.change_state("attack")
            else:
                self.entity.change_state("walk")

    def render(self, surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())

