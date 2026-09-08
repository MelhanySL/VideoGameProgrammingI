"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for game objects.
"""

from typing import Any, Dict

import settings


def _pickup_heart(player, obj) -> None:
    player.heal(2)
    settings.SOUNDS["heart-taken"].play()

def _pickup_bow(player, obj) -> None:
    player.has_bow = True
    settings.SOUNDS["collect_object"].play()


GAME_OBJECT_DEFS: Dict[str, Dict[str, Any]] = {
    "switch": {
        "type": "switch",
        "texture": "switches",
        "frame": 2,
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "unpressed",
        "states": {
            "unpressed": {"frame": 2},
            "pressed": {"frame": 1},
        },
    },
    "pot": {
        "type": "pot",
        "texture": "tiles",
        "frame": 16,
        "width": 16,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "default",
        "takeable": True,
        "states": {
            "default": {"frame": 16},
        },
    },
    # Definition of heart as a consumable object type.
    "heart": {
        "type": "heart",
        "texture": "hearts",
        "frame": 5,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": True,
        "default_state": "default",
        "states": {
            "default": {"frame": 5},
        },
        "on_consume": _pickup_heart,
    },
    "chest": {
        "type": "chest",
        "texture": "chests",
        "frame": 1,
        "width": 16,
        "height": 16,
        "solid": True,
        "default_state": "closed",
        "interactable": True,
        "states": {
            "open": {"frame": 4},
            "closed": {"frame": 1},
        },
        "animations": {
            "opening_chest": {
                "frames": [1, 2, 3, 4],
                "interval": 0.1,
                "loops": 1,
            }
        }
    },
    "bow": {
        "type": "bow",
        "texture": "bow",
        "frame": 1,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": True,
        "default_state": "default",
        "states": {
            "default": {"frame": 1},
        },
        "on_consume": _pickup_bow,
    },
    "arrow": {
        "type": "arrow",
        "texture": "arrow",
        "frame": 1,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": False,
        "default_state": "default",
        "takeable": False,
        "states": {
            "up": {"frame": 1},
            "down": {"frame": 3},
            "left": {"frame": 4},
            "right": {"frame": 2},
        },
    },
}
