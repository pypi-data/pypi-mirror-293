"""
ImportIO Client

This module provides a client for interacting with the ImportIO API.
It includes classes for handling extractors and crawl runs, as well as
utility functions and custom exceptions.

Classes:
    ImportIOError: Base exception for ImportIO errors.
    ExtractorNotFound: Exception for when an extractor is not found.
    StatusCodeError: Exception for unexpected status codes.
    FileType: Enum for different file types available in the API.
    ImportIOBase: Base class for ImportIO API interactions.
    ExtractorEndpoint: Class for interacting with ImportIO extractor endpoints.
    CrawlRunEndpoint: Class for interacting with ImportIO crawl run endpoints.
    ImportIOClient: Main client class for accessing ImportIO endpoints.

Functions:
    check_status_code: Decorator to check the status code of API responses.
    parse_response: Decorator to parse API responses.

Usage:
    client = ImportIOClient(api_key="your_api_key_here")
    extractor = client.extractor("your_extractor_id")
    crawl_run = client.crawl_run()
"""

from __future__ import annotations

import json
from enum import Enum, auto
from functools import wraps
from typing import Any, Callable, Dict, Union, List, Optional

import requests

class ImportIOError(Exception):
    """Base exception for ImportIO errors."""

class ExtractorNotFound(ImportIOError):
    """Raised when the specified extractor is not found."""

class StatusCodeError(ImportIOError):
    """Raised when an unexpected status code is received."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Status Code Error: {status_code} - {message}")

class FileType(Enum):
    """Enum for different file types available in the API."""
    CSV = auto()
    XLSX = auto()
    LOG = auto()
    SAMPLE = auto()
    JSON = auto()
    FILES = auto()

def check_status_code(func: Callable[..., requests.Response]) -> Callable[..., requests.Response]:
    """
    Decorator to check the status code of the response and handle errors.

    Args:
        func: The function to be decorated.

    Returns:
        A wrapper function that checks the status code and returns the response.

    Raises:
        StatusCodeError: If the status code is not 200.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> requests.Response:
        response = func(*args, **kwargs)
        if response.status_code != 200:
            raise StatusCodeError(response.status_code, response.text)
        return response
    return wrapper

def parse_response(
    parse_method: Union[str, Callable[[requests.Response], Any]] = 'json',
    default: Any = None
) -> Callable:
    """
    Decorator to parse the response from an API call.

    Args:
        parse_method: String ('json', 'text', 'content', 'jsonl') or a callable that takes a response object.
        default: Default value to return if parsing fails.

    Returns:
        A wrapper function that parses the response according to the specified method.
    """
    def decorator(func: Callable[..., requests.Response]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            response = func(*args, **kwargs)

            if callable(parse_method):
                return parse_method(response)

            if parse_method == 'json':
                try:
                    return response.json()
                except ValueError:
                    return default
            elif parse_method == 'text':
                return response.text
            elif parse_method == 'content':
                return response.content
            elif parse_method == 'jsonl':
                try:
                    return [json.loads(line) for line in response.text.splitlines() if line.strip()]
                except ValueError:
                    return default
            else:
                return response  # Return raw response if method is not recognized

        return wrapper
    return decorator

class ImportIOBase:
    """Base class for ImportIO API interactions."""

    def __init__(self, api_key: str):
        """
        Initialize the ImportIO instance.

        Args:
            api_key: The API key for authentication.
        """
        self.api_key = api_key
        self.params = {"_apikey": api_key}
        self.base_url = "https://api.import.io"

class ExtractorEndpoint(ImportIOBase):
    """Class for interacting with ImportIO extractor endpoints."""

    def __init__(self, api_key: str, extractor_id: str):
        """
        Initialize the ExtractorEndpoint instance.

        Args:
            api_key: The API key for authentication.
            extractor_id: The ID of the extractor.
        """
        super().__init__(api_key)
        self.id = extractor_id

    @parse_response('json')
    @check_status_code
    def set_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the inputs for the extractor.

        Args:
            inputs: A dictionary of input parameters for the extractor.

        Returns:
            A dictionary containing the API response.
        """
        return requests.put(
            f"{self.base_url}/extractors/{self.id}/inputs",
            params=self.params,
            json=inputs,
        )

    @parse_response('jsonl')
    @check_status_code
    def get_inputs(self) -> List[Dict[str, Any]]:
        """
        Get the inputs for the extractor.

        Returns:
            A list of dictionaries containing the current inputs for the extractor.
        """
        return requests.get(
            f"{self.base_url}/extractors/{self.id}/inputs",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def get_history(self) -> Dict[str, Any]:
        """
        Retrieve the run history for the extractor.

        Returns:
            A dictionary containing the run history for the extractor.
        """
        return requests.get(
            f"{self.base_url}/extractors/{self.id}/crawlruns",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def start_run(self) -> Dict[str, Any]:
        """
        Start a new run for the extractor.

        Returns:
            A dictionary containing information about the started run.
        """
        return requests.post(
            f"{self.base_url}/extractors/{self.id}/start",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def stop_run(self) -> Dict[str, Any]:
        """
        Stop the current run for the extractor.

        Returns:
            A dictionary containing information about the stopped run.
        """
        return requests.post(
            f"{self.base_url}/extractors/{self.id}/stop",
            params=self.params,
        )

class CrawlRunEndpoint(ImportIOBase):
    """Class for interacting with ImportIO crawl run endpoints."""

    @parse_response('json')
    @check_status_code
    def get_info(self, crawl_run_id: str) -> Dict[str, Any]:
        """
        Get information about a specific run.

        Args:
            crawl_run_id: The ID of the crawl run.

        Returns:
            A dictionary containing information about the specified crawl run.
        """
        return requests.get(
            f"{self.base_url}/crawlruns/{crawl_run_id}",
            params=self.params,
        )

    @parse_response('content')
    @check_status_code
    def get_file(self, crawl_run_id: str, file_type: FileType) -> bytes:
        """
        Get a specific file type for a run.

        Args:
            crawl_run_id: The ID of the crawl run.
            file_type: The type of file to retrieve (use FileType enum).

        Returns:
            The file content as bytes.
        """
        return requests.get(
            f"{self.base_url}/crawlruns/{crawl_run_id}/{file_type.name.lower()}",
            params=self.params,
        )

class ImportIOClient:
    """Client class for accessing ImportIO endpoints."""

    def __init__(self, api_key: str):
        """
        Initialize the ImportIOClient.

        Args:
            api_key: The API key for authentication.
        """
        self.api_key = api_key

    def extractor(self, extractor_id: str) -> ExtractorEndpoint:
        """
        Get an ExtractorEndpoint instance.

        Args:
            extractor_id: The ID of the extractor.

        Returns:
            An ExtractorEndpoint instance.
        """
        return ExtractorEndpoint(self.api_key, extractor_id)

    def crawl_run(self) -> CrawlRunEndpoint:
        """
        Get a CrawlRunEndpoint instance.

        Returns:
            A CrawlRunEndpoint instance.
        """
        return CrawlRunEndpoint(self.api_key)