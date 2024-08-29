# ImportIO Client

A Python client library for interacting with the ImportIO API.

## Installation

You can install the ImportIO Client using pip:

```
pip install importio-client
```

## Usage

Here's a basic example of how to use the ImportIO Client:

```python
from importio_client import ImportIOClient

# Initialize the client
client = ImportIOClient(api_key="your_api_key_here")

# Get an extractor
extractor = client.extractor("your_extractor_id")

# Start a run
run_info = extractor.start_run()
print(run_info)

# Get crawl run information
crawl_run = client.crawl_run()
info = crawl_run.get_info("your_crawl_run_id")
print(info)
```

For more detailed information, please refer to the documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.