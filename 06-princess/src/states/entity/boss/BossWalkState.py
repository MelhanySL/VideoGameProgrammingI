from src.states.entity.EntityWalkState import EntityWalkState
import random
import settings

class BossWalkState(EntityWalkState):

    def update(self, dt: float) -> None:
        super().update(dt)

        left_limit = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE
        right_limit = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2
        top_limit = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE + 16
        bottom_limit = settings.VIRTUAL_HEIGHT - settings.MAP_RENDER_OFFSET_Y - settings.TILE_SIZE

        if self.entity.x < left_limit:
            self.entity.x = left_limit
            self.bumped = True
        elif self.entity.x + self.entity.width > right_limit:
            self.entity.x = right_limit - self.entity.width
            self.bumped = True
            
        if self.entity.y < top_limit:
            self.entity.y = top_limit
            self.bumped = True
        elif self.entity.y + self.entity.height > bottom_limit:
            self.entity.y = bottom_limit - self.entity.height
            self.bumped = True

    def process_ai(self, room, dt) -> None:
            
        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.uniform(1, 2)
            self._pick_direction()
        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0

            if random.randint(1, 2) == 1:
                self.entity.change_state("attack")
                return
            else:
                self.entity.change_state("idle")
                return

        self.movement_timer += dt