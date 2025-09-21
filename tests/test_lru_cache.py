from src.cache.lru_cache import LRUCache

def test_lru_eviction_and_order():
    cache = LRUCache[int, str](capacity=2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"      # now 1 is MRU, 2 is LRU
    cache.put(3, "c")               # should evict key 2
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"

def test_update_moves_to_front():
    cache = LRUCache[int, str](capacity=2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(1, "a2")              # update value; 1 becomes MRU
    cache.put(3, "c")               # evicts key 2
    assert cache.get(2) is None
    assert cache.get(1) == "a2"
    assert cache.get(3) == "c"
