import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
from new import scrape_apartment_details
# Set up the Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



# Main page URL
main_page_url = 'https://www.immobilier.ch/fr/louer/appartement-maison/geneve/geneve/page-1?t=rent&c=1;2&p=c10377&pn=8000&nb=false&gr=1'

    # Navigate to the main page
driver.get(main_page_url)

try:
    # Find apartment links in the "Location" category and click on each
    apartment_links = driver.find_elements(By.CSS_SELECTOR, 'a[category="Location"]')
    for apartment_link in apartment_links:
        # Click on the apartment link
        apartment_link.click()
        time.sleep(5)  # Wait for the apartment page to load

        # Get the current URL of the apartment page
        apartment_page_url = driver.current_url
        
        # Call the scrape_apartment_details method with the apartment page URL
        scrape_apartment_details(apartment_page_url)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()