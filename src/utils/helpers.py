```python
import time
from typing import Optional

def parse_api_response_time(response_time: Optional[float]) -> str:
    """
    Converts API response time from milliseconds to a human-readable format.

    Args:
    response_time (Optional[float]): The response time in milliseconds.

    Returns:
    str: The response time in a human-readable format (e.g., 1.23ms, 123.45ms, 1.23s).
    """
    if response_time is None:
        return "N/A"

    if response_time < 1000:
        return f"{response_time:.2f}ms"
    else:
        return f"{response_time / 1000:.2f}s"

# Example usage:
response_time_ms = 1234.56
print(parse_api_response_time(response_time_ms))  # Output: 1.23s
```