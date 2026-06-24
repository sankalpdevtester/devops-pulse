import time
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a TTL (time to live) in seconds.

        Args:
        ttl (int): The time to live for each cache entry in seconds. Defaults to 60.
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        """
        Get a value from the cache.

        Args:
        key (str): The key of the value to retrieve.

        Returns:
        Any: The cached value or None if it does not exist or has expired.
        """
        if key in self.cache:
            value, expires = self.cache[key]
            if time.time() < expires:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        key (str): The key of the value to store.
        value (Any): The value to store.
        """
        expires = time.time() + self.ttl
        self.cache[key] = (value, expires)

    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.

        Args:
        key (str): The key of the value to delete.
        """
        if key in self.cache:
            del self.cache[key]

def get_cache() -> Cache:
    """
    Get the cache instance.

    Returns:
    Cache: The cache instance.
    """
    return Cache()

# Example usage:
cache = get_cache()
cache.set("api_response", {"status": 200, "data": {"message": "OK"}})
print(cache.get("api_response"))  # Output: {'status': 200, 'data': {'message': 'OK'}}
time.sleep(61)  # Wait for the TTL to expire
print(cache.get("api_response"))  # Output: None