import math
import settings
import pygame

class Fireball:
    def __init__(self, obj, target_x, target_y):
        self.obj = obj
        self.dead = False
        self.is_enemy_projectile = True
        
        center_x = self.obj.x + self.obj.width / 2
        center_y = self.obj.y + self.obj.height / 2
        
        angle = math.atan2(target_y - center_y, target_x - center_x)
        
        self.speed = 60
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def get_collision_rect(self):
        margin_x = 4
        margin_y = 4
        width = self.obj.width - (margin_x * 2)
        height = self.obj.height - (margin_y * 2)
        
        return pygame.Rect(
            round(self.obj.x + margin_x), 
            round(self.obj.y + margin_y), 
            width, 
            height
        )

    def update(self, dt):
        if self.dead:
            return

        if self.obj.current_animation:
            self.obj.current_animation.update(dt)

        self.obj.x += self.dx * dt
        self.obj.y += self.dy * dt
        
        if (self.obj.x <= settings.MAP_RENDER_OFFSET_X or 
            self.obj.x + self.obj.width >= settings.VIRTUAL_WIDTH - settings.MAP_RENDER_OFFSET_X or
            self.obj.y <= settings.MAP_RENDER_OFFSET_Y or
            self.obj.y + self.obj.height >= settings.VIRTUAL_HEIGHT - settings.MAP_RENDER_OFFSET_Y):
            self.dead = True

    def render(self, surface, offset_x=0, offset_y=0):
        self.obj.render(surface, offset_x, offset_y)

    def collides(self, target):
        return self.get_collision_rect().colliderect(target.get_collision_rect())