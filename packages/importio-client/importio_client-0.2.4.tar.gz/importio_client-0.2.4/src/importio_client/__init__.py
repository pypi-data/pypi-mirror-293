"""
ImportIO Client

This package provides a client for interacting with the ImportIO API.
"""

from .client import ImportIOClient, ExtractorEndpoint, CrawlRunEndpoint, FileType
from .exceptions import ImportIOError, ExtractorNotFound, StatusCodeError
from .utils import build_input_payload

__all__ = [
    'ImportIOClient',
    'ExtractorEndpoint',
    'CrawlRunEndpoint',
    'FileType',
    'ImportIOError',
    'ExtractorNotFound',
    'StatusCodeError',
    'build_input_payload'
]

__version__ = "0.2.4"  # Update this version number