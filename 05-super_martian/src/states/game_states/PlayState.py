"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)

        self.mask = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        self.mask.set_colorkey((255, 0, 255))

        self.max_radius = settings.VIRTUAL_WIDTH
        self.is_transitioning = False
        self.transition_radius = self.max_radius

        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            # Resting exactly on the ground tile's surface (row 9, one tile
            # below the platform's top edge) rather than a few pixels into
            # it, so gale.tilemap's one-way platform collision (which
            # requires the entity to already be at/above the surface) picks
            # it up on the very first frame instead of falling through.
            spawn_y = 9 * self.tilemap.tile_height - 20
            self.player = Player(0, spawn_y, self.game_level)
            self.player.change_state("idle")

            self.player.score = enter_params.get("score", 0)
            self.player.coins_counter = enter_params.get("coins", {54: 0, 55: 0, 61: 0, 62: 0})

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.follow(self.player, rate=settings.CAMERA_FOLLOW_RATE)
            self.camera.bounds = self.game_level.get_rect()
            self.camera.x, self.camera.y = self.player.x, self.player.y
            self.camera.update(0)

        self.clock = enter_params.get("clock")

        if self.clock is None:
            self.clock = Clock(60)

            def countdown_timer():
                if self.is_transitioning:
                    return
                
                self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")

            Timer.every(1, countdown_timer)

            if self.level > 1:
                self.is_transitioning = True
                self.transition_radius = 0

                def finish_iris_open():
                    self.is_transitioning = False

                Timer.tween(1.0, [(self, {"transition_radius": self.max_radius})], on_finish=finish_iris_open)

        else:
            Timer.resume()

    def update(self, dt: float) -> None:
        if self.is_transitioning:
            return
        
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)
        
        hitbox = self.player.get_collision_rect().move(0, -1) if (self.player.collided_y and not self.player.on_ground) else None
        active_blocks = []
        for block in self.game_level.blocks:
            if not block["spawned"] and self.player.score >= block["target_score"]:
                self.game_level.materialize_block(block)

            if block["spawned"] and block["active"] and hitbox and hitbox.colliderect(block["rect"]):
                block["active"] = False
                self.game_level.spawn_key(
                    block["rect"].x, 
                    block["rect"].y, 
                    block["empty_frame"]
                )
            
            if block["active"]:
                active_blocks.append(block)
                
        self.game_level.blocks = active_blocks

        self.camera.update(dt)
        self.game_level.update(dt)

        if self.player.y >= self.tilemap.pixel_height:
            self.player.change_state("dead")

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.active or not item.collidable:
                continue

            if self.player.collides(item):
                item.on_collide(self.player)
                item.on_consume(self.player)

                if item.frame_index == settings.KEY:
                    self.start_transition()

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        self.player.render(surface, self.camera)

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        if self.transition_radius < self.max_radius:
            self.mask.fill((0, 0, 0)) 
            center = (settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2)
            pygame.draw.circle(self.mask, (255, 0, 255), center, int(self.transition_radius))
            surface.blit(self.mask, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if self.is_transitioning:
            return
        
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)

    def start_transition(self) -> None:
        self.is_transitioning = True
        self.player.change_state("idle")
        self.player.vx = 0
        
        Timer.tween(
            1.5,
            [(self, {"transition_radius": 0})],
            on_finish=self.next_level
        )

    def next_level(self) -> None:
        def execute_level_change():
            Timer.clear() 
            if self.level < settings.NUM_LEVELS:
                self.state_machine.change(
                    "play", 
                    level=self.level + 1, 
                    score=self.player.score,
                    coins=self.player.coins_counter
                )
            else:
                self.state_machine.change("victory", self.player)
        Timer.after(0.01, execute_level_change)