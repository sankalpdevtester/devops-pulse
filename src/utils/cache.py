import time
from typing import Any, Dict

class Cache:
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.ttl: Dict[str, float] = {}

    def get(self, key: str) -> Any:
        """Get a value from the cache."""
        if key in self.cache:
            if key in self.ttl and self.ttl[key] < time.time():
                # Cache has expired, remove it
                del self.cache[key]
                del self.ttl[key]
                return None
            return self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """Set a value in the cache with a TTL."""
        self.cache[key] = value
        self.ttl[key] = time.time() + ttl

    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        if key in self.cache:
            del self.cache[key]
            if key in self.ttl:
                del self.ttl[key]

    def clear(self) -> None:
        """Clear the entire cache."""
        self.cache = {}
        self.ttl = {}

cache = Cache()

def get_cached_api_response(endpoint: str) -> Any:
    """Get a cached API response."""
    return cache.get(endpoint)

def cache_api_response(endpoint: str, response: Any, ttl: int = 60) -> None:
    """Cache an API response."""
    cache.set(endpoint, response, ttl)

def delete_cached_api_response(endpoint: str) -> None:
    """Delete a cached API response."""
    cache.delete(endpoint)

def clear_cached_api_responses() -> None:
    """Clear all cached API responses."""
    cache.clear()

# Example usage:
# cache_api_response("https://example.com/api/endpoint", {"data": "example"})
# print(get_cached_api_response("https://example.com/api/endpoint"))