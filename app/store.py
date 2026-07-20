import os
import time
import heapq
import asyncio
from typing import Optional, Tuple

MS_PER_SEC = 1000
EVICTION_TICK_RATE = 0.1
class DataStore:
    def __init__(self, aof_path: str = "database.aof") -> None:
        """initializes db state and triggers AOF recovery if possible"""
        # maps key -> (value, expiry_timestamp_ms)
        self._store: dict[str, Tuple[str, Optional[float]]] = {}

        self._expiry_heap: list[Tuple[float, str]] = []

        self.aof_path = aof_path
        self._restore_from_aof()

    def _append_to_aof(self, command_args:list[str]) -> None:
        """Logs a mutating command to the disk"""
        with open(self.aof_path, "a") as f:
            f.write(" ".join(command_args) + "\n")

    def _restore_from_aof(self) -> None:
        """Reads AOF to rebuild db state"""
        if not os.path.exists(self.aof_path):
            return
        
        print("RESTORING database state from {self.aof_path}...")

        with open(self.aof_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                cmd = parts[0].upper()
                if cmd == "SET" and len(parts) >= 3:
                    key, val = parts[1], parts[2]

                    px_val = None
                    if len(parts) >= 5 and parts[3].upper() == "PX":
                        try:
                            px_val = int(parts[4])
                        except ValueError:
                            pass
                    
                    self.set(key, val, px=px_val, log_to_aof=False)

    def set(self, key: str, value: str, px: Optional[int] = None, log_to_aof:bool = True) -> None:
        """Inserts or updates key-value pair into db, with optional TTL and logging

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

        if log_to_aof:
            command = ["SET", key, value]
            if px is not None:
                command.extend(["PX", str(px)])
            self._append_to_aof(command)

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