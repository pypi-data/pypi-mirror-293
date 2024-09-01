# memory_game_repository.py
from typing import Dict, Optional
from realm_keeper.models import GameRepository, GameWorld, GameObject

class MemoryGameRepository(GameRepository):
    def __init__(self):
        self.game_worlds: Dict[str, GameWorld] = {}
        self.game_objects: Dict[str, GameObject] = {}

    def save_game_world(self, game_world: GameWorld) -> None:
        self.game_worlds[game_world.id] = game_world

    def load_game_world(self, game_world_id: str) -> Optional[GameWorld]:
        return self.game_worlds.get(game_world_id)

    def save_game_object(self, game_object: GameObject) -> None:
        self.game_objects[game_object.id] = game_object

    def load_game_object(self, object_id: str) -> Optional[GameObject]:
        return self.game_objects.get(object_id)

    def delete_game_world(self, game_world_id: str) -> None:
        if game_world_id in self.game_worlds:
            game_world = self.game_worlds[game_world_id]
            for object_id in game_world.object_ids:
                self.game_objects.pop(object_id, None)
            self.game_worlds.pop(game_world_id, None)

    def delete_game_object(self, object_id: str) -> None:
        self.game_objects.pop(object_id, None)
