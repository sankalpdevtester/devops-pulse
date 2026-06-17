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
        key (str): The key to retrieve from the cache.

        Returns:
        Any: The cached value or None if it doesn't exist or has expired.
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
        key (str): The key to store in the cache.
        value (Any): The value to store in the cache.
        """
        expiry = time.time() + self.ttl
        self.cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
        key (str): The key to delete from the cache.
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
time.sleep(61)  # Wait for the cache to expire
print(cache.get("api_response"))  # Output: None
```
To integrate this cache utility with the existing files, you can use it in the `src/background_tasks.py` file to cache API responses. For example:
```python
from src.utils.cache import get_cache

cache = get_cache()

def fetch_api_response(api_url: str) -> Any:
    cached_response = cache.get(api_url)
    if cached_response:
        return cached_response
    else:
        response = requests.get(api_url)
        cache.set(api_url, response.json())
        return response.json()
```
You can also use the cache in the `src/models/endpoints.py` file to cache the results of expensive database queries. For example:
```python
from src.utils.cache import get_cache

cache = get_cache()

def get_endpoint_data(endpoint_id: int) -> Any:
    cached_data = cache.get(f"endpoint_data_{endpoint_id}")
    if cached_data:
        return cached_data
    else:
        data = EndpointModel.query.get(endpoint_id)
        cache.set(f"endpoint_data_{endpoint_id}", data)
        return data
```
This cache utility can be used throughout the project to improve performance by reducing the number of database queries and API requests.