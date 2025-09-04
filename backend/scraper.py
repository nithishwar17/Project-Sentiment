# backend/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon_reviews(url):
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    reviews = []
    review_selector = "[data-hook='review-body']"

    try:
        # --- STEP 1: Manual Login ---
        driver.get("https://www.amazon.in")
        print("\n" + "="*50)
        print("ACTION 1: Please log in to Amazon in the browser window.")
        input("After you have logged in, press Enter here to continue...")
        print("="*50 + "\n")
        
        # --- STEP 2: Navigate and wait for page to load ---
        print(f"Login complete. Navigating to product page: {url}")
        driver.get(url)
        
        print("\n" + "="*50)
        print("ACTION 2: The reviews page is loading.")
        input("Once the reviews are fully visible in the browser, press Enter here to begin scraping...")
        print("="*50 + "\n")

        # --- STEP 3: Scrape the visible data ---
        print("Scraping reviews...")
        # Now we just need to find the elements that are already loaded
        # A short wait is still good practice here.
        wait = WebDriverWait(driver, 10)
        review_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, review_selector)))
        print(f"Found {len(review_elements)} reviews on the page.")
        
        for element in review_elements:
            reviews.append(element.text)
            
    except Exception as e:
        print(f"An error occurred (check if the CSS selector '{review_selector}' is still correct): {e}")
        
    finally:
        driver.quit()

    return reviews