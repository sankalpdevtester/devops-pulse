```python
import re
from urllib.parse import urlparse

def validate_endpoint_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid API endpoint URL.
    
    Args:
    url (str): The URL to be validated.
    
    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and re.match(r'^/.*$', result.path)
    except ValueError:
        return False
```