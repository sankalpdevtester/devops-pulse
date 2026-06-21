import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a TTL (time to live) in seconds.

        Args:
        ttl (int): The time to live for each cache entry in seconds. Defaults to 60.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        key (str): The key to retrieve from the cache.

        Returns:
        Optional[Any]: The cached value if it exists and is not expired, otherwise None.
        """
        if key in self.cache:
            value = self.cache[key]
            if time.time() - value["timestamp"] < self.ttl:
                return value["data"]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        key (str): The key to store in the cache.
        value (Any): The value to store in the cache.
        """
        self.cache[key] = {"data": value, "timestamp": time.time()}

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        key (str): The key to delete from the cache.
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """
        Clear all entries from the cache.
        """
        self.cache.clear()

def get_cache() -> Cache:
    """
    Get the global cache instance.

    Returns:
    Cache: The global cache instance.
    """
    return Cache()

def cache_response(ttl: int = 60):
    """
    Decorator to cache API responses.

    Args:
    ttl (int): The time to live for the cached response in seconds. Defaults to 60.

    Returns:
    Callable: The decorated function.
    """
    cache = get_cache()

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_response = cache.get(key)
            if cached_response is not None:
                return cached_response
            response = func(*args, **kwargs)
            cache.set(key, response)
            return response
        return wrapper
    return decorator

# Example usage:
@cache_response(ttl=30)
def get_api_response():
    # Simulate an API call
    time.sleep(1)
    return {"data": "API response"}

print(get_api_response())  # Cache miss
print(get_api_response())  # Cache hit