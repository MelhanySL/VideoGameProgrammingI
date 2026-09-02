"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the game settings that include the association of the
inputs with an their ids, constants of values to set up the game, sounds,
textures, and fonts.
"""

from pathlib import Path

import pygame

from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "confirm")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "jump")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "pause")

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "right")

TITLE = "Flappy Bird"

# Size of our actual window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Size we are trying to emulate
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288

BIRD_WIDTH = 39
BIRD_HEIGHT = 28
BIRD_HORIZONTAL_SPEED = 200 

LOG_CLOSE_SPEED = 70 
LOG_OPEN_SPEED = 50 

HARD_MODE_LOG_MARGIN_TOP = 20
HARD_MODE_LOG_MARGIN_BOTTOM = 20
HARD_MODE_GHOST_MIN_INTERVAL = 5.0
HARD_MODE_GHOST_MAX_INTERVAL = 20.0
HARD_MODE_INITIAL_LOG_SPAWN_DELAY = 1.5

GHOST_WIDTH = 30
GHOST_HEIGHT = 27
GHOSTING_TIME = 5.0

LOG_WIDTH = 70
LOG_HEIGHT = 288
LOGS_GAP = 90

GROUND_HEIGHT = 16

# Vertical range a log pair's top-log y may take (see World.update). The
# lower bound keeps a sliver of the top log's edge on screen; the upper
# bound keeps the full LOGS_GAP opening above the ground -- without it, a
# pair could spawn so low the top log's bottom edge sits at or past the
# ground, leaving no passable opening at all.
MIN_LOG_Y = -LOG_HEIGHT + 10
MAX_LOG_Y = VIRTUAL_HEIGHT - GROUND_HEIGHT - LOGS_GAP - LOG_HEIGHT

BACKGROUND_LOOPING_POINT = 1157

MAIN_SCROLL_SPEED = 100
BACK_SCROLL_SPEED = 50  # MAIN_SCROLL_SPEED / 2

GRAVITY = 980
JUMP_TAKEOFF_SPEED = GRAVITY / 6

TIME_TO_SPAWN_LOGS = 1.5

MEDIUM_TEXT_SIZE = 18
HUGE_TEXT_SIZE = 56
FLAPPY_TEXT_SIZE = 28

BASE_DIR = Path(__file__).parent

TEXTURES = {
    "bird": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bird.png"),
    "background": pygame.image.load(BASE_DIR / "assets" / "graphics" / "background.png"),
    "ground": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ground.png"),
    "log": pygame.image.load(BASE_DIR / "assets" / "graphics" / "log.png"),
    "ghost": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ghost.png"),
    "ghost_bird": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ghost_bird.png"),
}
# The top log of every pair is the same image, flipped upside down.
TEXTURES["log_inverted"] = pygame.transform.flip(TEXTURES["log"], False, True)

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "explosion": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "explosion.wav"),
    "hurt": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "hurt.wav"),
    "score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "score.wav"),
    "select": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "select.wav"),
    "confirm": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "confirm.wav"),
    "collide": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "creaky_door.wav"),
    "ghost_music": pygame.mixer.Sound(BASE_DIR / "assets"/ "sounds" / "booster_sound.wav"),
}

pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "marios_way.ogg")

FONTS = {
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", MEDIUM_TEXT_SIZE),
    "huge": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", HUGE_TEXT_SIZE),
    "flappy": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "flappy.ttf", FLAPPY_TEXT_SIZE
    ),
}

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
