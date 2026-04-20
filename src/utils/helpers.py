```python
import re
from urllib.parse import urlparse

def validate_api_endpoint_url(url: str) -> bool:
    """
    Validate API endpoint URL.
    
    Args:
    url (str): The URL to be validated.
    
    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and re.match(r'^https?$', result.scheme)
    except ValueError:
        return False

def validate_string(input_string: str, min_length: int = 1, max_length: int = 100) -> bool:
    # existing function
    pass
```