import time
import heapq
import asyncio
from typing import Optional, Tuple

MS_PER_SEC = 1000
EVICTION_TICK_RATE = 0.1
class DataStore:
    def __init__(self) -> None:
        """initializes db state"""
        # maps key -> (value, expiry_timestamp_ms)
        self._store: dict[str, Tuple[str, Optional[float]]] = {}

        self._expiry_heap: list[Tuple[float, str]] = []

    def set(self, key: str, value: str, px: Optional[int] = None) -> None:
        """Inserts or updates key-value pair into db, with optional TTL

        Args:
            key (str): identifier for the payload
            value (str): payload to store
            px (int, optional): TTL in ms
        """
        expiry_time = None
        if px is not None:
            expiry_time = (time.time() * MS_PER_SEC) + px
            heapq.heappush(self._expiry_heap, (expiry_time, key))
        self._store[key] = (value, expiry_time)

    def get(self, key:str) -> Optional[str]:
        """Retrieves a value by key

        Args:
            key (str): identifier to look up

        Returns:
            str | None: stored val or None if it doesn't exist
        """
        if key not in self._store:
            return None
        
        value, expiry_time = self._store[key]
        
        if expiry_time is not None and (time.time() * MS_PER_SEC) > expiry_time:
            del self._store[key]
            return None
        
        return value
    
    def exists(self, key:str) -> bool:
        """Checks if key exists in storage"""
        return key in self._store
    
# creating a global singleton of the store
# since asyncio is single threaded the dict
# shouldn't have issues with race conditions

db = DataStore()