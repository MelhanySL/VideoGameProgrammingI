"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""

import random

import pygame

from gale.factory import AbstractFactory
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

import settings
import src.powerups

from src.Bullet import Bullet


class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])

        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")

        self.bullets = params.get("bullets", [])
        self.shield_active = params.get("shield_active", False)
        self.shield_height = 12

        self.shield_texture = pygame.Surface((settings.VIRTUAL_WIDTH, self.shield_height), pygame.SRCALPHA)
        self.shield_texture.fill((0, 150, 255))
        self.shield_texture.set_alpha(150)

    def update(self, dt: float) -> None:
        self.paddle.update(dt)

        for ball in self.balls:

            if ball.caught:
                ball.x = self.paddle.x + ball.caught_x
                ball.y = self.paddle.y - ball.height
                if not self.paddle.ball_caught:
                    ball.caught = False
                    ball.vy = random.randint(-170, -100)
                    ball.vx = random.randint(-80, 80)
                    continue
            ball.update(dt)

            if self.shield_active and ball.y > settings.VIRTUAL_HEIGHT - ball.height:
                ball.y = settings.VIRTUAL_HEIGHT - ball.height - self.shield_height
                ball.vy = -abs(ball.vy)
                settings.SOUNDS["wall_hit"].stop()
                settings.SOUNDS["wall_hit"].play()
                settings.SOUNDS["broken"].play()
                self.shield_active = False
            else:
                ball.solve_world_boundaries()

            # Check collision with the paddle
            if ball.collides(self.paddle):

                if self.paddle.ball_caught:
                    ball.caught = True
                    ball.caught_x = ball.x - self.paddle.x
                else: 
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)


            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            # Chance to generate two more balls
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("BallCatch").create(
                        r.centerx - 8, r.centery - 8
                    )
                )

            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("CannonPower").create(
                        r.centerx - 8, r.centery - 8
                    )
                )

            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("ShieldPower").create(
                        r.centerx - 8, r.centery - 8
                    )
                )

        for bullet in self.bullets:
            bullet.update(dt)

            if not bullet.active:
                continue
            
            if not bullet.collides(self.brickset):
                continue

            
            brick = self.brickset.get_colliding_brick(bullet.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            bullet.active = False
            self.score += brick.score()
            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()


        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.active]

        self.bullets = [bullet for bullet in self.bullets if bullet.active]

        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.active]

        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        self.brickset.render(surface)

        self.paddle.render(surface)

        if self.shield_active:
            surface.blit(self.shield_texture, (0, settings.VIRTUAL_HEIGHT - self.shield_height))

        for ball in self.balls:
            ball.render(surface)

        for bullet in self.bullets:
            bullet.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "pause" and input_data.pressed:
            ball_caughts = [ball for ball in self.balls if ball.caught]
            
            if ball_caughts:
                for ball in ball_caughts:
                    ball.caught = False
                    ball.vy = random.randint(-170, -100)
                    ball.vx = random.randint(-80, 80)

            else:
                self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
                bullets=self.bullets,
                shield_active=self.shield_active,
            )
        elif input_id == "shoot" and input_data.pressed:
            if self.paddle.cannon_active and len(self.bullets) == 0:
                left_bullet_x = self.paddle.x + self.paddle.cannon_size // 2 - 4
                right_bullet_x = self.paddle.x + self.paddle.width - self.paddle.cannon_size // 2 - 4
                bullet_y = self.paddle.y - (self.paddle.cannon_size // 2)

                self.bullets.append(Bullet(left_bullet_x, bullet_y))
                self.bullets.append(Bullet(right_bullet_x, bullet_y))
            