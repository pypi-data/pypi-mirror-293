from abc import ABC, abstractmethod
from typing import Optional
from .game_object import GameObject
from .game_world import GameWorld

class GameRepository(ABC):
    @abstractmethod
    def save_game_world(self, game_world: GameWorld) -> None:
        pass

    @abstractmethod
    def load_game_world(self, game_world_id: str) -> Optional[GameWorld]:
        pass

    @abstractmethod
    def save_game_object(self, game_object: GameObject) -> None:
        pass

    @abstractmethod
    def load_game_object(self, object_id: str) -> Optional[GameObject]:
        pass

    @abstractmethod
    def delete_game_world(self, game_world_id: str) -> None:
        pass

    @abstractmethod
    def delete_game_object(self, object_id: str) -> None:
        pass
