import pytest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

# Assuming your module is my_package.browser
from my_package.browser import get_chrome_driver, find_element_by_id

@patch('my_package.browser.ChromeDriverManager')
@patch('my_package.browser.webdriver.Chrome')
def test_get_chrome_driver_success(mock_chrome, mock_chrome_driver_manager):
    mock_install_instance = MagicMock()
    # The install method is on the instance returned by ChromeDriverManager()
    mock_chrome_driver_manager.return_value.install.return_value = "/fake/driver/path"
    
    mock_driver_instance = MagicMock()
    mock_chrome.return_value = mock_driver_instance
    
    driver = get_chrome_driver()
    
    mock_chrome_driver_manager.assert_called_once()
    mock_chrome_driver_manager.return_value.install.assert_called_once()
    # Check that options are passed to Chrome constructor
    mock_chrome.assert_called_once()
    args, kwargs = mock_chrome.call_args
    assert 'options' in kwargs
    assert kwargs['options'] is not None
    assert driver == mock_driver_instance

@patch('my_package.browser.ChromeDriverManager')
@patch('my_package.browser.webdriver.Chrome') # Mock Chrome to ensure it's not actually called if manager fails
def test_get_chrome_driver_manager_exception(mock_chrome, mock_chrome_driver_manager):
    # Simulate an exception during ChromeDriverManager().install()
    mock_chrome_driver_manager.return_value.install.side_effect = Exception("Install failed")
    
    driver = get_chrome_driver()
    
    mock_chrome_driver_manager.assert_called_once()
    mock_chrome_driver_manager.return_value.install.assert_called_once()
    mock_chrome.assert_not_called() # webdriver.Chrome should not be called if install fails
    assert driver is None

@patch('my_package.browser.ChromeDriverManager') # Keep this to mock the installation part
@patch('my_package.browser.webdriver.Chrome')
def test_get_chrome_driver_chrome_exception(mock_chrome, mock_chrome_driver_manager):
    # Simulate ChromeDriverManager().install() succeeding
    mock_chrome_driver_manager.return_value.install.return_value = "/fake/driver/path"
    # Simulate an exception during webdriver.Chrome() initialization
    mock_chrome.side_effect = Exception("Chrome init failed")
    
    driver = get_chrome_driver()
    
    mock_chrome_driver_manager.assert_called_once()
    mock_chrome_driver_manager.return_value.install.assert_called_once()
    mock_chrome.assert_called_once() # webdriver.Chrome is called but raises an exception
    assert driver is None


def test_find_element_by_id_success():
    mock_driver = MagicMock()
    mock_element_instance = MagicMock() # This will be the WebElement
    mock_driver.find_element.return_value = mock_element_instance
    
    url = "http://example.com"
    element_id = "test_id"
    
    element = find_element_by_id(mock_driver, url, element_id)
    
    mock_driver.get.assert_called_once_with(url)
    mock_driver.find_element.assert_called_once_with(By.ID, element_id)
    assert element == mock_element_instance

def test_find_element_by_id_no_such_element():
    mock_driver = MagicMock()
    # Configure the mock_driver's find_element method to raise NoSuchElementException
    mock_driver.find_element.side_effect = NoSuchElementException("Element not found")
    
    url = "http://example.com"
    element_id = "test_id"
    
    element = find_element_by_id(mock_driver, url, element_id)
    
    mock_driver.get.assert_called_once_with(url)
    mock_driver.find_element.assert_called_once_with(By.ID, element_id)
    assert element is None

def test_find_element_by_id_driver_get_exception(): # Renamed for clarity
    mock_driver = MagicMock()
    # Configure the mock_driver's get method to raise a generic Exception (could be TimeoutException too)
    mock_driver.get.side_effect = Exception("Page load failed")
    
    url = "http://example.com"
    element_id = "test_id" # This won't be reached if get() fails
    
    element = find_element_by_id(mock_driver, url, element_id)
    
    mock_driver.get.assert_called_once_with(url)
    # find_element should not be called if get() fails
    mock_driver.find_element.assert_not_called() 
    assert element is None

def test_find_element_by_id_no_driver():
    # Test the initial check for a valid driver object
    element = find_element_by_id(None, "http://example.com", "test_id")
    assert element is None
