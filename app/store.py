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
        return self.get(key) is not None
    
    async def eviction_loop(self) -> None:
        """Daemon task to remove expired keys. Runs alongside TCP server"""
        while True:
            if not self._expiry_heap:
                await asyncio.sleep(EVICTION_TICK_RATE)
                continue

            current_ms = time.time() * MS_PER_SEC
            smallest_expiry, key = self._expiry_heap[0]

            if current_ms > smallest_expiry:
                heapq.heappop(self._expiry_heap)

                if key in self._store:
                    _, actual_expiry = self._store[key]
                    if actual_expiry == smallest_expiry:
                        del self._store[key]
                        print(f"Eviction Loop: Purged expired key '{key}'")

            else:
                sleep_time = (smallest_expiry - current_ms) / float(MS_PER_SEC)
                await asyncio.sleep(min(sleep_time, EVICTION_TICK_RATE))
    
# creating a global singleton of the store
# since asyncio is single threaded the dict
# shouldn't have issues with race conditions

db = DataStore()