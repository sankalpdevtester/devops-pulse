import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, ttl: int = 60):
        """
        Initialize the cache with a TTL (time to live) in seconds.

        :param ttl: The time to live for each cache entry in seconds.
        """
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        :param key: The key to retrieve from the cache.
        :return: The cached value or None if not found or expired.
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

        :param key: The key to store in the cache.
        :param value: The value to store in the cache.
        """
        expires = time.time() + self.ttl
        self.cache[key] = (value, expires)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        :param key: The key to delete from the cache.
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

    :return: The global cache instance.
    """
    if not hasattr(get_cache, 'instance'):
        get_cache.instance = Cache()
    return get_cache.instance


def cache_api_response(ttl: int = 60):
    """
    Decorator to cache API responses.

    :param ttl: The time to live for the cache entry in seconds.
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
@cache_api_response(ttl=30)
def get_api_response():
    # Simulate an API call
    time.sleep(1)
    return {"status": "ok"}

print(get_api_response())  # Cache miss
print(get_api_response())  # Cache hit