```python
import re
from typing import Optional

def validate_api_endpoint_url(url: str) -> Optional[str]:
    """
    Validate API endpoint URL.

    Args:
    url (str): The URL to be validated.

    Returns:
    Optional[str]: Error message if the URL is invalid, otherwise None.
    """
    # Check if the URL starts with http or https
    if not re.match(r"^https?", url):
        return "URL must start with http or https"

    # Check if the URL contains any invalid characters
    if not re.match(r"^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(/[^\/\s]+)*$", url):
        return "URL contains invalid characters"

    return None

# Example usage:
def validate_url_example():
    url = "https://example.com/api/endpoint"
    error = validate_api_endpoint_url(url)
    if error:
        print(f"Invalid URL: {error}")
    else:
        print("URL is valid")

# Other existing utility functions...
```