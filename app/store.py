class DataStore:
    def __init__(self) -> None:
        """initializes db state"""
        self._store: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        """Inserts or updates key-value pair into db

        Args:
            key (str): identifier for the payload
            value (str): payload to store
        """
        self._store[key] = value

    def get(self, key:str) -> str | None:
        """Retrieves a value by key

        Args:
            key (str): identifier to look up

        Returns:
            str | None: stored val or None if it doesn't exist
        """
        return self._store.get(key)
    
    def exists(self, key:str) -> bool:
        """Checks if key exists in storage"""
        return key in self._store
    
# creating a global singleton of the store
# since asyncio is single threaded the dict
# shouldn't have issues with race conditions

db = DataStore()