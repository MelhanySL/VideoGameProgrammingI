from src.powerups.PowerUp import PowerUp
import settings
import pygame

class ColorBomb(PowerUp):
    def activate(self, board) -> set:
        tiles_to_destroy = set()
        
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                tile = board.tiles[i][j]
                
                if tile is not None and tile.color == self.color:
                    tiles_to_destroy.add(tile)
                    
        return tiles_to_destroy

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
            super().render(surface, offset_x, offset_y)
            
            center_margin = (settings.TILE_SIZE - settings.ICON_SIZE) // 2
            
            if self.dragging:
                draw_x = self.drag_x + center_margin
                draw_y = self.drag_y + center_margin
            else:
                draw_x = self.x + offset_x + center_margin
                draw_y = self.y + offset_y + center_margin
                
            surface.blit(settings.TEXTURES["color_bomb"], (draw_x, draw_y))