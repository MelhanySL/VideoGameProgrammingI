from .FlappyModes import FlappyGameMode
from gale.input_handler import InputData
from src.LogPair import LogPair
from collections import namedtuple

import settings
import random

LogProfile = namedtuple(
    "LogProfile",
    "weight moving gap_min gap_max spawn_min spawn_max vertical_shift",
)

class HardMode(FlappyGameMode):
    PROFILES = [
        LogProfile(40, True, 110, 130, 1.5, 2.0, 45),
        LogProfile(18, False, 80, 90, 1.8, 2.4, 50),
        LogProfile(24, False, 80, 100, 1.4, 1.8, 40),
        LogProfile(18, False, 100, 120, 1.0, 1.6, 30),
    ]

    def __init__(self):
        self.next_log_spawn_delay = settings.HARD_MODE_INITIAL_LOG_SPAWN_DELAY
        self.ghost_elapsed_time = 0.0
        self.next_ghost_spawn_delay = random.uniform(settings.HARD_MODE_GHOST_MIN_INTERVAL, settings.HARD_MODE_GHOST_MAX_INTERVAL)

    def update_world(self, world, dt) -> None:
            world.generate_logs = False
            world.logs_spawn_timer += dt
            self.ghost_elapsed_time += dt
    
            if world.logs_spawn_timer >= self.next_log_spawn_delay:
                self._spawn_log_pair(world)
    
            if self.ghost_elapsed_time >= self.next_ghost_spawn_delay:
                self._spawn_ghost(world)
    
    def _choose_log_profile(self) -> LogProfile:
        weights = [profile.weight for profile in self.PROFILES]
        return random.choices(self.PROFILES, weights=weights, k=1)[0]

    def _spawn_log_pair(self, world) -> None:
        profile = self._choose_log_profile()
        gap = random.randint(profile.gap_min, profile.gap_max)
        self.next_log_spawn_delay = random.uniform(profile.spawn_min, profile.spawn_max)
        world.logs_spawn_timer = 0.0

        y = max(
            -settings.LOG_HEIGHT + settings.HARD_MODE_LOG_MARGIN_TOP,
            min(
                world.last_log_y + random.randint(-profile.vertical_shift, profile.vertical_shift),
                settings.VIRTUAL_HEIGHT - gap - settings.LOG_HEIGHT - settings.HARD_MODE_LOG_MARGIN_BOTTOM - settings.GROUND_HEIGHT
            )
        )
        world.last_log_y = y

        log_pair: LogPair = world.log_pair_factory.create(settings.VIRTUAL_WIDTH, y)
        log_pair.gap = gap
        log_pair.original_gap = gap
        log_pair.move = profile.moving
        world.logs.append(log_pair)

    def _spawn_ghost(self, world) -> None:
        if world.logs:
            last_log = world.logs[-1]
            gap_center = last_log.y + settings.LOG_HEIGHT + (last_log.gap / 2)
            ghost_y = int(gap_center - (settings.GHOST_HEIGHT / 2))
        else:
            ghost_y = settings.VIRTUAL_HEIGHT / 2

        world.spawn_ghost(settings.VIRTUAL_WIDTH + settings.GHOST_WIDTH, ghost_y)
        self.next_ghost_spawn_delay = random.uniform(
            settings.HARD_MODE_GHOST_MIN_INTERVAL,
            settings.HARD_MODE_GHOST_MAX_INTERVAL,
        )
        self.ghost_elapsed_time = 0.0

    def on_input(self, bird, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            bird.jump()
            return

        if input_id == "left":
            bird.vx = -settings.BIRD_HORIZONTAL_SPEED if input_data.pressed else 0
            return

        if input_id == "right":
            bird.vx = settings.BIRD_HORIZONTAL_SPEED if input_data.pressed else 0