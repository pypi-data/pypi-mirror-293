# ImportIO Client

A Python client library for interacting with the ImportIO API. This client provides an easy-to-use interface for managing extractors and crawl runs.

## Installation

You can install the ImportIO Client using pip:

```bash
pip install importio-client
```

## Usage

Here's a quick start guide to using the ImportIO Client:

```python
from importio_client import ImportIOClient

# Initialize the client
client = ImportIOClient(api_key="your_api_key_here")

# Working with extractors
extractor_id = "your_extractor_id"

# Set inputs for an extractor
client.extractor.set_inputs(extractor_id, "https://example.com")

# Set inputs with default attributes
client.extractor.set_inputs(
    extractor_id,
    ["https://example.com", "https://another.com"],
    default_attributes={"Max Screens": 50, "Browser": "chrome"}
)

# Start a run
run_info = client.extractor.start_run(extractor_id)
print(run_info)

# Get extractor history
history = client.extractor.get_history(extractor_id)
print(history)

# Working with crawl runs
crawl_run_id = "your_crawl_run_id"

# Get crawl run information
crawl_info = client.crawl_run.get_info(crawl_run_id)
print(crawl_info)

# Get a file from a crawl run
from importio_client import FileType
file_content = client.crawl_run.get_file(crawl_run_id, FileType.CSV)
```

## Features

- Easy-to-use interface for ImportIO API
- Support for extractor operations (set inputs, start/stop runs, get history)
- Support for crawl run operations (get info, retrieve files)
- Flexible input handling for extractors, including support for default attributes
- Built-in error handling and response parsing

## API Reference

### ImportIOClient

The main client class for interacting with the ImportIO API.

#### Methods:

- `__init__(api_key: str)`: Initialize the client with your API key.

### ExtractorEndpoint

Accessible via `client.extractor`.

#### Methods:

- `set_inputs(extractor_id: str, inputs: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]], default_attributes: Dict[str, Any] = None) -> Dict[str, Any]`: Set inputs for an extractor.
- `get_inputs(extractor_id: str) -> List[Dict[str, Any]]`: Get current inputs for an extractor.
- `get_history(extractor_id: str) -> Dict[str, Any]`: Get run history for an extractor.
- `start_run(extractor_id: str) -> Dict[str, Any]`: Start a new run for an extractor.
- `stop_run(extractor_id: str) -> Dict[str, Any]`: Stop the current run for an extractor.

### CrawlRunEndpoint

Accessible via `client.crawl_run`.

#### Methods:

- `get_info(crawl_run_id: str) -> Dict[str, Any]`: Get information about a specific crawl run.
- `get_file(crawl_run_id: str, file_type: FileType) -> bytes`: Get a specific file type for a crawl run.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.