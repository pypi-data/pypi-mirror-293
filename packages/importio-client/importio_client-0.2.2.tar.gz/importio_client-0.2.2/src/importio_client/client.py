"""
client.py

This module provides the main client for interacting with the ImportIO API.
It includes classes for handling extractors and crawl runs.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Dict, List, Union

import requests

from .utils import build_input_payload, check_status_code, parse_response

class FileType(Enum):
    """Enum for different file types available in the API."""
    CSV = auto()
    XLSX = auto()
    LOG = auto()
    SAMPLE = auto()
    JSON = auto()
    FILES = auto()

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

    @parse_response('json')
    @check_status_code
    def set_inputs(
        self, 
        extractor_id: str, 
        inputs: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]],
        default_attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Update the inputs for the extractor.
        
        Args:
            extractor_id: The ID of the extractor.
            inputs: Can be a single URL string, a list of URL strings,
                    a dictionary with '_url' key, or a list of such dictionaries.
            default_attributes: A dictionary of key-value pairs to be added to each input.
        
        Returns:
            A dictionary containing the API response.
        """
        payload = build_input_payload(inputs, default_attributes)
        
        return requests.put(
            f"{self.base_url}/extractors/{extractor_id}/inputs",
            params=self.params,
            data=payload,
            headers={"Content-Type": "application/x-ndjson"}
        )

    @parse_response('jsonl')
    @check_status_code
    def get_inputs(self, extractor_id: str) -> List[Dict[str, Any]]:
        """
        Get the inputs for the extractor.

        Args:
            extractor_id: The ID of the extractor.

        Returns:
            A list of dictionaries containing the current inputs for the extractor.
        """
        return requests.get(
            f"{self.base_url}/extractors/{extractor_id}/inputs",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def get_history(self, extractor_id: str) -> Dict[str, Any]:
        """
        Retrieve the run history for the extractor.

        Args:
            extractor_id: The ID of the extractor.

        Returns:
            A dictionary containing the run history for the extractor.
        """
        return requests.get(
            f"{self.base_url}/extractors/{extractor_id}/crawlruns",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def start_run(self, extractor_id: str) -> Dict[str, Any]:
        """
        Start a new run for the extractor.

        Args:
            extractor_id: The ID of the extractor.

        Returns:
            A dictionary containing information about the started run.
        """
        return requests.post(
            f"{self.base_url}/extractors/{extractor_id}/start",
            params=self.params,
        )

    @parse_response('json')
    @check_status_code
    def stop_run(self, extractor_id: str) -> Dict[str, Any]:
        """
        Stop the current run for the extractor.

        Args:
            extractor_id: The ID of the extractor.

        Returns:
            A dictionary containing information about the stopped run.
        """
        return requests.post(
            f"{self.base_url}/extractors/{extractor_id}/stop",
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
        self.extractor = ExtractorEndpoint(api_key)
        self.crawl_run = CrawlRunEndpoint(api_key)