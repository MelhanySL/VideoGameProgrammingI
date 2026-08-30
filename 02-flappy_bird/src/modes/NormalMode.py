from .FlappyModes import FlappyGameMode
from gale.input_handler import InputData

class NormalMode(FlappyGameMode):
    def update_world(self, world, dt) -> None:
        pass
        
    def on_input(self, bird, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            bird.jump()