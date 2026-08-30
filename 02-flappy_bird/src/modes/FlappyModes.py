from abc import ABC, abstractmethod
from gale.input_handler import InputData
from src.World import World
from src.Bird import Bird

class FlappyGameMode(ABC):
    @abstractmethod
    def update_world(self, world: World, dt: float) -> None:
        pass

    @abstractmethod
    def on_input(self, bird: Bird, input_id: str, input_data: InputData) -> None:
        pass
