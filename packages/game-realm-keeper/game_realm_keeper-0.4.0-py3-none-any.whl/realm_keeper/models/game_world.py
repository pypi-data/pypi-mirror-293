# game_world.py
from typing import Dict, Any, List, Optional, Set
from .game_object import GameObject
from pydantic import BaseModel, Field


class GameWorld(BaseModel):
    id: str
    object_ids: Set[str] = Field(default_factory=set)
    rules: List[str] = Field(default_factory=list)

    def add_object_id(self, object_id: str):
        self.object_ids.add(object_id)

    def remove_object_id(self, object_id: str):
        self.object_ids.discard(object_id)

    def add_rule(self, rule: str):
        self.rules.append(rule)

    def get_rules(self) -> List[str]:
        return self.rules.copy()
