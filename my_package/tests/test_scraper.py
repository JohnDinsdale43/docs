import pytest
from unittest.mock import patch, MagicMock
from my_package.scraper import get_page_title
import requests

# Define a class to hold mock response attributes
class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Mock HTTP Error {self.status_code}")

@patch('my_package.scraper.requests.get')
def test_get_page_title_success(mock_get):
    # Mock successful response
    mock_response = MockResponse(b"<html><head><title>Test Title</title></head><body></body></html>", 200)
    mock_get.return_value = mock_response
    
    title = get_page_title("http://example.com")
    assert title == "Test Title"
    mock_get.assert_called_once_with("http://example.com", timeout=10)

@patch('my_package.scraper.requests.get')
def test_get_page_title_no_title_tag(mock_get):
    # Mock response with no title tag
    mock_response = MockResponse(b"<html><head></head><body></body></html>", 200)
    mock_get.return_value = mock_response
    
    title = get_page_title("http://example.com")
    assert title is None

@patch('my_package.scraper.requests.get')
def test_get_page_title_http_error(mock_get):
    # Mock response for an HTTP error
    mock_response = MockResponse(None, 404)
    mock_get.return_value = mock_response
    
    # Ensure that raise_for_status is called and an HTTPError is raised by the mock
    # We need to mock the instance's method, not the class's, if get_page_title calls it on the instance
    # If get_page_title directly calls response.raise_for_status(), this is correct.
    mock_response.raise_for_status = MagicMock(side_effect=requests.exceptions.HTTPError("Mock HTTP Error"))
    
    title = get_page_title("http://example.com")
    assert title is None # Expect None because the error is caught and handled in get_page_title

@patch('my_package.scraper.requests.get')
def test_get_page_title_request_exception(mock_get):
    # Mock requests.get to raise a RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Mock network error")
    
    title = get_page_title("http://example.com")
    assert title is None
