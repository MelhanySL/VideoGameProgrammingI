from src.states.entity.BaseEntityState import BaseEntityState

class BossDeathState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation(f"death-{self.entity.direction}")
        self.timer = 0
        
    def process_ai(self, room, dt: float) -> None:
        if self.entity.current_animation.times_played > 0:
            self.entity.dead = True

    def render(self, surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())