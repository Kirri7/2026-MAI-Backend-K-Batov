# from typing import Any, Dict
from collections import OrderedDict

# Least Recently Used
class LRUCache:
    def __init__(self, capacity: int=10) -> None:
        self._capacity : int = capacity
        self._cache : OrderedDict[str, str] = OrderedDict() # better call Saul for FIFO!

    def get(self, key: str) -> str:
        return self._cache.get(key, '')

    def set(self, key: str, value: str) -> None:
        self._cache[key] = value
        self._clear_cache()

    def rem(self, key: str) -> None:
        self._cache.pop(key, None)

    def _clear_cache(self) -> None:
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False) # FIFO
        
        