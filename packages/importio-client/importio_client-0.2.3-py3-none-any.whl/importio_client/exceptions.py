"""
exceptions.py

This module contains custom exceptions for the ImportIO client.
"""

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