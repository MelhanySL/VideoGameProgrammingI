from src.states.entity.BaseEntityState import BaseEntityState
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.GameObject import GameObject
from src.Fireball import Fireball

class BossAttackState(BaseEntityState):
    def enter(self):
        self.entity.change_animation(f"attack-{self.entity.direction}")
        self.shoot_timer = 0.5
        self.shots_fired = 0

    def process_ai(self, room, dt):
        self.shoot_timer += dt

        if self.shoot_timer >= 0.5 and self.shots_fired < 3:
            self.shots_fired += 1
            self.shoot_timer = 0
            
            fireball_def = GAME_OBJECT_DEFS.get("fireball", GAME_OBJECT_DEFS["arrow"])
            fireball_obj = GameObject(fireball_def, self.entity.x, self.entity.y)

            fireball_obj.current_animation = fireball_obj.animations["fire"]
            
            target_x = room.player.x + room.player.width / 2
            target_y = room.player.y + room.player.height / 2
            
            projectile = Fireball(fireball_obj, target_x, target_y)
            room.projectiles.append(projectile)

        if self.shoot_timer > 0.7 and self.shots_fired >= 3:
            self.entity.change_state("idle")

    def render(self, surface):
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())