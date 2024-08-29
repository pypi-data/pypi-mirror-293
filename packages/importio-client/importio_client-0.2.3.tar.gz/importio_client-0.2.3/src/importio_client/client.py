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

        :param api_key: The API key for authentication.

        Args:
            api_key (str): The API key for authentication with the ImportIO service.
        """
        self.api_key = api_key
        self.params = {"_apikey": api_key}
        self.base_url = "https://api.import.io"

class ExtractorEndpoint(ImportIOBase):
    """Class for interacting with ImportIO extractor endpoints."""

    @check_status_code
    @parse_response('json')
    def set_inputs(
        self, 
        extractor_id: str, 
        inputs: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]],
        default_attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Update the inputs for the extractor.

        :param extractor_id: The ID of the extractor.
        :param inputs: Input data for the extractor.
        :param default_attributes: Default attributes to apply to all inputs.
        :return: A dictionary containing the API response.

        Args:
            extractor_id (str): The unique identifier of the extractor.
            inputs (Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]]): 
                Can be a single URL string, a list of URL strings,
                a dictionary with '_url' key, or a list of such dictionaries.
            default_attributes (Dict[str, Any], optional): A dictionary of key-value pairs 
                to be added to each input. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the API response.
        """
        payload = build_input_payload(inputs, default_attributes)

        return requests.put(
            f"{self.base_url}/extractors/{extractor_id}/inputs",
            params=self.params,
            data=payload,
            headers={"Content-Type": "application/x-ndjson"}
        )

    @check_status_code
    @parse_response('jsonl')
    def get_inputs(self, extractor_id: str) -> List[Dict[str, Any]]:
        """
        Get the inputs for the extractor.

        :param extractor_id: The ID of the extractor.
        :return: A list of dictionaries containing the current inputs for the extractor.

        Args:
            extractor_id (str): The unique identifier of the extractor.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing 
            the details of an input for the specified extractor.
        """
        return requests.get(
            f"{self.base_url}/extractors/{extractor_id}/inputs",
            params=self.params,
        )

    @check_status_code
    @parse_response('json')
    def get_history(self, extractor_id: str) -> Dict[str, Any]:
        """
        Retrieve the run history for the extractor.

        :param extractor_id: The ID of the extractor.
        :return: A dictionary containing the run history for the extractor.

        Args:
            extractor_id (str): The unique identifier of the extractor.

        Returns:
            Dict[str, Any]: A dictionary containing the run history for the extractor,
            including details of past runs and their outcomes.
        """
        return requests.get(
            f"{self.base_url}/extractors/{extractor_id}/crawlruns",
            params=self.params,
        )

    @check_status_code
    @parse_response('json')
    def start_run(self, extractor_id: str) -> Dict[str, Any]:
        """
        Start a new run for the extractor.

        :param extractor_id: The ID of the extractor.
        :return: A dictionary containing information about the started run.

        Args:
            extractor_id (str): The unique identifier of the extractor.

        Returns:
            Dict[str, Any]: A dictionary containing information about the started run,
            such as the run ID and start time.
        """
        return requests.post(
            f"{self.base_url}/extractors/{extractor_id}/start",
            params=self.params,
        )

    @check_status_code
    @parse_response('json')
    def stop_run(self, extractor_id: str) -> Dict[str, Any]:
        """
        Stop the current run for the extractor.

        :param extractor_id: The ID of the extractor.
        :return: A dictionary containing information about the stopped run.

        Args:
            extractor_id (str): The unique identifier of the extractor.

        Returns:
            Dict[str, Any]: A dictionary containing information about the stopped run,
            such as the run ID and stop time.
        """
        return requests.post(
            f"{self.base_url}/extractors/{extractor_id}/stop",
            params=self.params,
        )

class CrawlRunEndpoint(ImportIOBase):
    """Class for interacting with ImportIO crawl run endpoints."""

    @check_status_code
    @parse_response('json')
    def get_info(self, crawl_run_id: str) -> Dict[str, Any]:
        """
        Get information about a specific run.

        :param crawl_run_id: The ID of the crawl run.
        :return: A dictionary containing information about the specified crawl run.

        Args:
            crawl_run_id (str): The unique identifier of the crawl run.

        Returns:
            Dict[str, Any]: A dictionary containing detailed information about 
            the specified crawl run, including its status and results.
        """
        return requests.get(
            f"{self.base_url}/crawlruns/{crawl_run_id}",
            params=self.params,
        )

    @check_status_code
    @parse_response('content')
    def get_file(self, crawl_run_id: str, file_type: FileType) -> bytes:
        """
        Get a specific file type for a run.

        :param crawl_run_id: The ID of the crawl run.
        :param file_type: The type of file to retrieve (use FileType enum).
        :return: The file content as bytes.

        Args:
            crawl_run_id (str): The unique identifier of the crawl run.
            file_type (FileType): The type of file to retrieve, specified using the FileType enum.

        Returns:
            bytes: The content of the requested file as a bytes object.
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

        :param api_key: The API key for authentication.

        Args:
            api_key (str): The API key for authentication with the ImportIO service.
        """
        self.api_key = api_key
        self.extractor = ExtractorEndpoint(api_key)
        self.crawl_run = CrawlRunEndpoint(api_key)