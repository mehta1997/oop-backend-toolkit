from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Dict

K = TypeVar("K")
V = TypeVar("V")

@dataclass
class _Node(Generic[K, V]):
    key: K
    value: V
    prev: Optional["_Node[K, V]"] = None
    next: Optional["_Node[K, V]"] = None


class LRUCache(Generic[K, V]):
    """A classic OOP LRU cache with O(1) get/put.
    Uses a doubly linked list + dict. Thread-safety can be added with a Lock if needed.
    """
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self._map: Dict[K, _Node[K, V]] = {}
        # dummy head/tail to simplify edge logic
        self._head = _Node[K, V](key=None, value=None)  # type: ignore[arg-type]
        self._tail = _Node[K, V](key=None, value=None)  # type: ignore[arg-type]
        self._head.next = self._tail
        self._tail.prev = self._head

    # ----- Doubly-linked list helpers -----
    def _add_front(self, node: _Node[K, V]) -> None:
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node  # type: ignore[union-attr]
        self._head.next = node

    def _remove(self, node: _Node[K, V]) -> None:
        prev = node.prev
        nxt = node.next
        if prev: prev.next = nxt
        if nxt: nxt.prev = prev
        node.prev = node.next = None

    def _move_to_front(self, node: _Node[K, V]) -> None:
        self._remove(node)
        self._add_front(node)

    def _pop_lru(self) -> Optional[_Node[K, V]]:
        lru = self._tail.prev
        if lru is self._head:
            return None
        if lru:
            self._remove(lru)
        return lru

    # ----- Public API -----
    def get(self, key: K) -> Optional[V]:
        node = self._map.get(key)
        if not node:
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        node = self._map.get(key)
        if node:
            node.value = value
            self._move_to_front(node)
            return
        node = _Node(key, value)
        self._map[key] = node
        self._add_front(node)
        if len(self._map) > self.capacity:
            lru = self._pop_lru()
            if lru:
                self._map.pop(lru.key, None)

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: K) -> bool:
        return key in self._map
