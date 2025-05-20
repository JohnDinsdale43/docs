import requests
from bs4 import BeautifulSoup

def get_page_title(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            return title_tag.string.strip()
        return None # Or raise an error if title is expected
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    target_url = 'https://www.autotrader.co.uk'
    print(f"Fetching title for: {target_url}")
    title = get_page_title(target_url)
    if title:
        print(f"Page Title: {title}")
    else:
        print("Could not retrieve the page title.")
