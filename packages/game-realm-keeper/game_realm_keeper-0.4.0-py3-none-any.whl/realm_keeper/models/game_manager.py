# game_manager.py
from typing import Any, Dict, List, Optional
from uuid import uuid4
from .game_repository import GameRepository
from .game_world import GameWorld
from .game_object import GameObject


class GameManager:
    def __init__(self, game_world_id: str, repository: GameRepository):
        self.game_world_id = game_world_id
        self.repository = repository
        self.game_world = self.repository.load_game_world(game_world_id) or GameWorld(
            id=game_world_id
        )

    def save_state(self):
        self.repository.save_game_world(self.game_world)

    def create_character(self, name: str) -> str:
        char_id = str(uuid4())
        character = GameObject(id=char_id, type="character", attributes={"name": name})
        self.repository.save_game_object(character)
        self.game_world.add_object_id(char_id)
        self.save_state()
        return f"Created character '{name}' with ID {char_id}"

    def create_item(self, name: str) -> str:
        item_id = str(uuid4())
        item = GameObject(id=item_id, type="item", attributes={"name": name})
        self.repository.save_game_object(item)
        self.game_world.add_object_id(item_id)
        self.save_state()
        return f"Created item '{name}' with ID {item_id}"

    def get_object(self, object_id: str) -> Optional[GameObject]:
        return self.repository.load_game_object(object_id)

    def update_object(self, game_object: GameObject) -> None:
        self.repository.save_game_object(game_object)

    def set_attribute(self, object_id: str, attribute: str, value: Any) -> str:
        obj = self.get_object(object_id)
        if obj:
            obj.attributes[attribute] = value
            self.update_object(obj)
            return f"Set {attribute} to {value} for object {object_id}"
        return f"Object {object_id} not found"

    def equip_item(self, character_id: str, item_id: str, slot: str) -> str:
        character = self.get_object(character_id)
        item = self.get_object(item_id)
        if character and item:
            if character.type != "character":
                return f"Object {character_id} is not a character"
            if item.type != "item":
                return f"Object {item_id} is not an item"
            character.equipment[slot] = item_id
            self.update_object(character)
            return f"Equipped {item.attributes['name']} to {character.attributes['name']} in slot {slot}"
        return "Character or item not found"

    def get_game_state(self) -> Dict[str, Any]:
        state = self.game_world.model_dump()
        state["objects"] = {
            obj_id: self.get_object(obj_id).model_dump()
            for obj_id in self.game_world.object_ids
        }
        state["rules"] = self.game_world.get_rules()  # 添加這行
        return state

    def get_formatted_game_state(self) -> str:
        state = self.get_game_state()
        formatted_state = f"Game World ID: {state['id']}\nCurrent game state:\n"
        if state["rules"]:
            formatted_state += "Rules:\n"
            for rule in state["rules"]:
                formatted_state += f"- {rule}\n"
            formatted_state += "\n"
        for obj_id, obj in state["objects"].items():
            formatted_state += (
                f"- {obj['attributes'].get('name', 'Unnamed')} ({obj['type']}):\n"
            )
            for attr, value in obj["attributes"].items():
                if attr != "name":
                    formatted_state += f"  {attr}: {value}\n"
            if obj["equipment"]:
                formatted_state += "  Equipment:\n"
                for slot, equipped_id in obj["equipment"].items():
                    equipped_item = self.get_object(equipped_id)
                    if equipped_item:
                        formatted_state += f"    {slot}: {equipped_item.attributes.get('name', 'Unnamed')}\n"
        return formatted_state

    def add_rule(self, rule: str) -> str:
        self.game_world.add_rule(rule)
        self.save_state()
        return f"Added rule: {rule}"

    def get_rules(self) -> str:
        rules = self.game_world.get_rules()
        if rules:
            return "Game Rules:\n" + "\n".join(f"- {rule}" for rule in rules)
        return "No rules defined yet."

    def remove_object(self, object_id: str) -> str:
        obj = self.get_object(object_id)
        if obj:
            self.game_world.remove_object_id(object_id)
            self.repository.delete_game_object(object_id)
            self.save_state()
            return f"Removed object {obj.attributes.get('name', 'Unnamed')} with ID {object_id}"
        return f"Object {object_id} not found"

    def list_objects(self, object_type: str = None) -> str:
        objects = [self.get_object(obj_id) for obj_id in self.game_world.object_ids]
        filtered_objects = (
            objects
            if object_type is None
            else [obj for obj in objects if obj.type == object_type]
        )

        if not filtered_objects:
            return (
                f"No objects found{' of type ' + object_type if object_type else ''}."
            )

        result = f"{'All objects' if object_type is None else object_type.capitalize() + 's'}:\n"
        for obj in filtered_objects:
            result += f"- {obj.attributes.get('name', 'Unnamed')} (ID: {obj.id})\n"
        return result
