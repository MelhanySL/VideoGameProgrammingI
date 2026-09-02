from src.powerups.PowerUp import PowerUp
import settings
import pygame

class LineClear(PowerUp):
    def activate(self, board) -> set:
        tiles_to_destroy = set()

        for row in range(settings.BOARD_HEIGHT):
            if board.tiles[row][self.j] is not None:
                tiles_to_destroy.add(board.tiles[row][self.j])
                
        for col in range(settings.BOARD_WIDTH):
            if board.tiles[self.i][col] is not None:
                tiles_to_destroy.add(board.tiles[self.i][col])
                
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
            
        surface.blit(settings.TEXTURES["line_clear"], (draw_x, draw_y))