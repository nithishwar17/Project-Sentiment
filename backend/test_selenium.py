# backend/test_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("--- Starting Basic Selenium Test ---")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print("Browser launched successfully. Navigating to Google.")
    driver.get("https://www.google.com")

    time.sleep(3) # Wait for 3 seconds

    print(f"Page Title: {driver.title}")
    print("Test PASSED! Selenium can open Chrome.")

except Exception as e:
    print("Test FAILED!")
    print(f"An error occurred: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
    print("--- Test Finished ---")