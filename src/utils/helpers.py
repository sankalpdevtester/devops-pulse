import logging
from typing import Any

# Define a logger
logger = logging.getLogger(__name__)

def api_request(endpoint: str, method: str = 'GET', data: Any = None) -> Any:
    """
    Makes a request to the specified API endpoint.

    Args:
    - endpoint (str): The API endpoint to make the request to.
    - method (str): The HTTP method to use (default: 'GET').
    - data (Any): The data to send with the request (default: None).

    Returns:
    - Any: The response from the API.
    """
    try:
        # Make the API request
        if method == 'GET':
            response = requests.get(endpoint)
        elif method == 'POST':
            response = requests.post(endpoint, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        # Check if the request was successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log the error and re-raise it
        logger.error(f"API request failed: {e}")
        raise
    except Exception as e:
        # Log the error and re-raise it
        logger.error(f"An error occurred: {e}")
        raise

def parse_api_response(response: Any) -> dict:
    """
    Parses the API response and returns a dictionary.

    Args:
    - response (Any): The API response.

    Returns:
    - dict: The parsed API response.
    """
    try:
        # Try to parse the response as JSON
        return response.json()
    except AttributeError:
        # If the response is not a JSON object, return an empty dictionary
        return {}
    except Exception as e:
        # Log the error and re-raise it
        logger.error(f"Failed to parse API response: {e}")
        raise

# Add a small helper function to check if a string is a valid URL
def is_valid_url(url: str) -> bool:
    """
    Checks if a string is a valid URL.

    Args:
    - url (str): The string to check.

    Returns:
    - bool: True if the string is a valid URL, False otherwise.
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False