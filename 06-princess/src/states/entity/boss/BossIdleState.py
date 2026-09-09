from src.states.entity.EntityIdleState import EntityIdleState
import random

class BossIdleState(EntityIdleState):
    def process_ai(self, room, dt):
        if self.wait_duration == 0:
            self.wait_duration = 5
        else:
            self.wait_timer += dt
            if self.wait_timer > self.wait_duration:

                if random.randint(1, 2) == 1:
                    self.entity.change_state("attack")
                else:
                    self.entity.change_state("walk")