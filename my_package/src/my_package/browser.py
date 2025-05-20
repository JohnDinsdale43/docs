from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_chrome_driver():
    '''Initializes and returns a Selenium Chrome WebDriver instance.'''
    try:
        options = webdriver.ChromeOptions()
        # Add any desired options here (e.g., headless mode)
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox') # Recommended for running in containers
        options.add_argument('--disable-dev-shm-usage') # Recommended for running in containers
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        return None

def find_element_by_id(driver, url: str, element_id: str):
    '''Navigates to URL and finds an element by its ID.'''
    if not driver:
        print("WebDriver not initialized.")
        return None
    try:
        driver.get(url)
        element = driver.find_element(By.ID, element_id)
        return element
    except TimeoutException:
        print(f"Timeout while loading URL: {url}")
        return None
    except NoSuchElementException:
        print(f"Element with ID '{element_id}' not found on {url}")
        return None
    except Exception as e:
        print(f"An error occurred while trying to find element ID '{element_id}' on {url}: {e}")
        return None

if __name__ == '__main__':
    driver = get_chrome_driver()
    if driver:
        try:
            autotrader_url = 'https://www.autotrader.co.uk'
            # This is a conceptual ID. The actual ID on autotrader.co.uk for the postcode
            # or search input will likely be different and may require inspection.
            search_input_id = 'postcode' 
            
            print(f"Attempting to navigate to: {autotrader_url}")
            print(f"Looking for element with conceptual ID: '{search_input_id}'")
            
            element = find_element_by_id(driver, autotrader_url, search_input_id)
            
            if element:
                print(f"Conceptually found element with ID '{search_input_id}'. Element tag: {element.tag_name}")
                # Further interactions could be added here, e.g. element.send_keys("TEST")
            else:
                print(f"Could not conceptually find element with ID '{search_input_id}'. "
                      "This might be because the ID is incorrect, the page structure changed, "
                      "or the element is loaded dynamically.")
        finally:
            print("Closing browser.")
            driver.quit()
    else:
        print("Failed to initialize WebDriver.")
