```python
"""
Helper functions for API requests and error handling.
"""

import requests
from typing import Dict

def make_api_request(url: str, method: str = 'GET', data: Dict = None) -> Dict:
    """
    Makes an API request to the specified URL.

    Args:
    - url (str): The URL of the API endpoint.
    - method (str): The HTTP method to use (default: 'GET').
    - data (Dict): The data to send with the request (default: None).

    Returns:
    - Dict: The JSON response from the API.

    Raises:
    - requests.RequestException: If the request fails.
    """
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Log the error and re-raise the exception
        print(f"API request failed: {e}")
        raise
```