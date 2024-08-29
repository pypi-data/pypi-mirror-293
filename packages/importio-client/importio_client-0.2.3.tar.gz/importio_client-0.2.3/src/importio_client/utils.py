"""
utils.py

This module contains utility functions for the ImportIO client.
"""

import json
from functools import wraps
from typing import Any, Callable, Dict, List, Union

import requests
from .exceptions import StatusCodeError

def build_input_payload(
    inputs: Union[str, List[str], Dict[str, Any], List[Dict[str, Any]]],
    default_attributes: Dict[str, Any] = None
) -> str:
    """
    Build the correct input payload for the API, with optional default attributes.
    
    Args:
        inputs: Can be a single URL string, a list of URL strings,
                a dictionary with '_url' key, or a list of such dictionaries.
        default_attributes: A dictionary of key-value pairs to be added to each input.
    
    Returns:
        A string formatted as expected by the API.
    """
    default_attributes = default_attributes or {}

    def process_input(input_item: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(input_item, str):
            input_item = {"_url": input_item}
        return {**default_attributes, **input_item}

    if isinstance(inputs, (str, dict)):
        inputs = [inputs]
    
    processed_inputs = [process_input(item) for item in inputs]
    return "\n".join(json.dumps(item) for item in processed_inputs)

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