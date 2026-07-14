import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a time-to-live (TTL) value.

        Args:
        - ttl (int): The time-to-live value in seconds. Defaults to 60.
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
        - key (str): The key to retrieve the value for.

        Returns:
        - The cached value if it exists and is not expired, otherwise None.
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
        - key (str): The key to store the value under.
        - value (Any): The value to store.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        - key (str): The key to delete.
        """
        if key in self.cache:
            del self.cache[key]

def get_cache() -> Cache:
    """
    Get the cache instance.

    Returns:
    - The cache instance.
    """
    return Cache()

def cache_response(ttl: int = 60):
    """
    Decorator to cache API responses.

    Args:
    - ttl (int): The time-to-live value in seconds. Defaults to 60.
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
    time.sleep(2)
    return {"status": "ok"}

print(get_api_response())  # Cache miss
print(get_api_response())  # Cache hit