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
        Any: The cached value or None if it doesn't exist or has expired.
        """
        if key in self.cache:
            value, expires_at = self.cache[key]
            if time.time() < expires_at:
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
        expires_at = time.time() + self.ttl
        self.cache[key] = (value, expires_at)

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
    Get the global cache instance.

    Returns:
    Cache: The global cache instance.
    """
    cache = Cache()
    return cache

# Example usage:
cache = get_cache()
cache.set("api_response", {"status": 200, "data": {"message": "OK"}})
print(cache.get("api_response"))  # Output: {'status': 200, 'data': {'message': 'OK'}}
```
To integrate this cache utility with the existing files, you can use it in the `src/background_tasks.py` file to cache API responses. For example:
```python
from src.utils.cache import get_cache

cache = get_cache()

def fetch_api_data():
    # Fetch API data
    api_response = fetch_api()
    cache.set("api_response", api_response)
    return api_response

def get_api_data():
    cached_response = cache.get("api_response")
    if cached_response:
        return cached_response
    else:
        return fetch_api_data()
```
You can also use the cache utility in the `src/pages/addEndpoint.tsx` file to cache API endpoint data. For example:
```typescript
import { getCache } from '../utils/cache';

const cache = getCache();

const AddEndpointPage = () => {
  const [endpointData, setEndpointData] = useState({});

  const fetchEndpointData = async () => {
    const cachedResponse = cache.get('endpoint_data');
    if (cachedResponse) {
      setEndpointData(cachedResponse);
    } else {
      const response = await fetch('/api/endpoint');
      const data = await response.json();
      cache.set('endpoint_data', data);
      setEndpointData(data);
    }
  };

  return (
    <div>
      <h1>Add Endpoint</h1>
      <button onClick={fetchEndpointData}>Fetch Endpoint Data</button>
      <pre>{JSON.stringify(endpointData, null, 2)}</pre>
    </div>
  );
};
```
Note that you need to modify the `src/utils/helpers.py` file to include the cache utility. You can add the following code to the file:
```python
from src.utils.cache import get_cache

def get_cache():
    return get_cache()
```
This will allow you to use the cache utility in the `src/background_tasks.py` file.