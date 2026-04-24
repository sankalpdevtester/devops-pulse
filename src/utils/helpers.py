```python
import json
from typing import Dict

def parse_api_response_time(api_response: Dict) -> float:
    """
    Parse API response time from the response dictionary.

    Args:
    api_response (Dict): API response dictionary containing 'response_time' key.

    Returns:
    float: API response time in milliseconds.
    """
    if 'response_time' in api_response:
        return api_response['response_time']
    elif 'timing' in api_response and 'response' in api_response['timing']:
        return api_response['timing']['response']
    else:
        raise ValueError("API response time not found in the response dictionary")

def parse_json(data: str) -> Dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

# existing code...
```