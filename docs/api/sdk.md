# xnLinkFinder-Z Python SDK Documentation

## Installation

```bash
pip install xnlinkfinder
```

## Quick Start

```python
from xnLinkFinder.sdk import XnLinkFinderClient

# Initialize client
client = XnLinkFinderClient(
    base_url="http://localhost:8080",
    api_key="your_api_key"
)

# Start a scan
scan = client.scan("https://example.com")
print(f"Scan ID: {scan['scan_id']}")

# Get results
results = client.get_results(scan['scan_id'])
print(f"Found {len(results['results'])} endpoints")
```

## API Reference

### XnLinkFinderClient

#### `__init__(base_url, api_key=None)`
Initialize the SDK client.

**Parameters:**
- `base_url` (str): API server URL
- `api_key` (str, optional): API authentication key

#### `scan(url, **kwargs)`
Start a new scan.

**Parameters:**
- `url` (str): Target URL
- `**kwargs`: Additional scan options

**Returns:**
- dict: Scan information including `scan_id`

#### `get_results(scan_id)`
Get scan results.

**Parameters:**
- `scan_id` (str): Scan identifier

**Returns:**
- dict: Scan results

#### `scan_async(url, **kwargs)`
Async version of scan method.

## Examples

### Basic Scan
```python
client = XnLinkFinderClient()
result = client.scan("https://example.com")
```

### With Security Scanning
```python
result = client.scan(
    "https://example.com",
    scan_cors=True,
    scan_jwt=True
)
```

### Async Usage
```python
import asyncio

async def main():
    client = XnLinkFinderClient()
    result = await client.scan_async("https://example.com")
    print(result)

asyncio.run(main())
```
