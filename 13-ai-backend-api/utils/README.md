# Utils

This directory contains utility functions and decorators.

## Retry Decorator

The `retry_async` decorator provides retry logic with exponential backoff for async functions.

### Usage

```python
from utils.retry import retry_async

@retry_async(
    max_retries=3,
    delay=1.0,
    backoff_factor=2.0,
    exceptions=(Exception,)
)
async def unreliable_function():
    # Function that might fail
    pass
```

### Parameters

- **max_retries**: Maximum number of retry attempts (default: 3)
- **delay**: Initial delay between retries in seconds (default: 1.0)
- **backoff_factor**: Multiplier for delay after each retry (default: 2.0)
- **exceptions**: Tuple of exception types to catch and retry (default: (Exception,))

### Example

```python
from utils.retry import retry_async
import aiohttp

@retry_async(
    max_retries=3,
    delay=1.0,
    backoff_factor=2.0,
    exceptions=(aiohttp.ClientError, TimeoutError)
)
async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Behavior

1. If the function succeeds, the result is returned immediately
2. If the function raises a retryable exception:
   - Wait `delay * (backoff_factor ** attempt)` seconds
   - Retry the function
3. If all retries fail, the last exception is raised

### Exponential Backoff

The delay between retries increases exponentially:

- Attempt 1: 1.0 seconds
- Attempt 2: 2.0 seconds
- Attempt 3: 4.0 seconds
- Attempt 4: 8.0 seconds
- etc.