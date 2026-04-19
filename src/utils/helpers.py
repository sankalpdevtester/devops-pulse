import logging
from typing import Dict, Any

def handle_api_error(error: Dict[str, Any]) -> None:
    """
    Handles API errors by logging the error message and status code.
    
    Args:
    error (Dict[str, Any]): A dictionary containing the error message and status code.
    """
    try:
        error_message = error.get("message", "Unknown error")
        status_code = error.get("status_code", 500)
        logging.error(f"API error {status_code}: {error_message}")
    except Exception as e:
        # Log any unexpected errors
        logging.error(f"Unexpected error handling API error: {str(e)}")

def api_request(url: str, method: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Makes an API request to the specified URL with the given method and data.
    
    Args:
    url (str): The URL of the API endpoint.
    method (str): The HTTP method to use (e.g., GET, POST, PUT, DELETE).
    data (Dict[str, Any], optional): The data to send with the request. Defaults to None.
    
    Returns:
    Dict[str, Any]: The response from the API.
    """
    try:
        # Make the API request (implementation omitted for brevity)
        response = {"status_code": 200, "message": "OK"}
        return response
    except Exception as e:
        # Handle any errors that occur during the request
        error = {"message": str(e), "status_code": 500}
        handle_api_error(error)
        return error