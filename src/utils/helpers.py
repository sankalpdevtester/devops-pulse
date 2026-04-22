```python
import time
from typing import Dict

def parse_api_response_time(response_time: float) -> Dict[str, float]:
    """
    Parse API response time into milliseconds, seconds, and minutes.

    Args:
    response_time (float): Response time in seconds.

    Returns:
    Dict[str, float]: Dictionary containing response time in milliseconds, seconds, and minutes.
    """
    response_time_ms = response_time * 1000
    response_time_min = response_time / 60

    return {
        "ms": response_time_ms,
        "s": response_time,
        "min": response_time_min
    }

def get_current_timestamp() -> int:
    # existing function
    return int(time.time())

# existing functions...
```