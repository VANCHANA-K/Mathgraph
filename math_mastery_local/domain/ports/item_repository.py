from typing import Protocol

from domain.entities.item import Item


class ItemRepository(Protocol):
    def list_items_by_topic(self, topic_id: str) -> list[Item]: ...
    def get_item(self, item_id: str) -> Item | None: ...
