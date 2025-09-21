from __future__ import annotations
from collections import OrderedDict
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class LRUCache(Generic[K, V]):
    """A simple LRU (Least Recently Used) cache with fixed capacity."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        # move key to the end (most recently used)
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        if key in self._data:
            # update existing and move to end
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            # pop least recently used item (first one)
            self._data.popitem(last=False)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: K) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, items={list(self._data.items())})"
