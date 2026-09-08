from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.GameObject import GameObject

class Bow:
    def init(self):
        self.arrow_factory = self

    def create_arrow(self, player):
        arrow_def = GAME_OBJECT_DEFS["arrow"]

        x = player.x
        y = player.y

        if player.direction == "left":
            x -= 8
        elif player.direction == "right":
            x += player.width
        elif player.direction == "up":
            y -= 8
        elif player.direction == "down":
            y += player.height

        arrow = GameObject(
            x=x,
            y=y,
            width=arrow_def["width"],
            height=arrow_def["height"],
            texture_id=arrow_def["texture"],
            type=arrow_def["type"],
        )

        arrow.direction = player.direction
        arrow.owner = "player"
        arrow.damage = 1
        arrow.speed = 180
        arrow.dead = False

        return arrow

    def fire(self, player, room):
        arrow = self.create_arrow(player)
        room.projectiles.append(arrow)