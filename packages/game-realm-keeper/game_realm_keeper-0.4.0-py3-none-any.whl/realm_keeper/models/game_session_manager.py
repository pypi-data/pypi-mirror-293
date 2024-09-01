# game_session_manager.py
from typing import Dict
from uuid import uuid4
from .game_repository import GameRepository
from .game_manager import GameManager
from .game_world import GameWorld

class GameSessionManager:
    def __init__(self, repository: GameRepository):
        self.repository = repository
        self.active_games: Dict[str, GameManager] = {}

    def create_game(self) -> str:
        game_world_id = str(uuid4())
        game_world = GameWorld(id=game_world_id)
        self.repository.save_game_world(game_world)
        game_manager = GameManager(game_world_id, self.repository)
        self.active_games[game_world_id] = game_manager
        return game_world_id

    def get_game_manager(self, game_world_id: str) -> GameManager:
        if game_world_id not in self.active_games:
            game_world = self.repository.load_game_world(game_world_id)
            if game_world:
                self.active_games[game_world_id] = GameManager(game_world_id, self.repository)
            else:
                raise ValueError(f"No game found with id {game_world_id}")
        return self.active_games[game_world_id]

    def end_game_session(self, game_world_id: str) -> bool:
        if game_world_id in self.active_games:
            del self.active_games[game_world_id]
            return True
        return False

    def delete_game(self, game_world_id: str) -> bool:
        if game_world_id in self.active_games:
            del self.active_games[game_world_id]
        self.repository.delete_game_world(game_world_id)
        return True
