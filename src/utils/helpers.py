```python
import urllib.parse

def parse_api_endpoint_url(url: str) -> dict:
    """
    Parse an API endpoint URL into its components.

    Args:
    url (str): The API endpoint URL to parse.

    Returns:
    dict: A dictionary containing the parsed URL components.
    """
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    return {
        "scheme": parsed_url.scheme,
        "netloc": parsed_url.netloc,
        "path": parsed_url.path,
        "query_params": query_params
    }
```