from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
from new import scrape_apartment_details

# Set up the Chrome driver
driver = webdriver.Chrome()

# URL of the main page
main_page_url = 'https://www.immobilier.ch/fr/louer/appartement-maison/geneve/geneve/page-1?t=rent&c=1;2&p=c10377&pn=8000&nb=false'

# Navigate to the main page
driver.get(main_page_url)

# List to store all apartment URLs
all_apartment_urls = []
count = 0
# Loop through the pages to collect URLs
while True:
    # Wait for the page to load
    time.sleep(2)  # Adjust this sleep duration as needed

    # Find apartment links with specific id attributes
    apartment_links = driver.find_elements(By.CSS_SELECTOR, 'a[id^="link-result-item-"][category="Location"]')
    
    # Extract and store the href attributes
    for link in apartment_links:
        href = link.get_attribute("href")
        all_apartment_urls.append(href)

    try:
        # Find the 'Next' button and click it
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
        next_button.click()
        count = count + 1
        print("Navigating to next page...{count}")
    except NoSuchElementException:
        # If 'Next' button is not found, exit the loop
        print("Collected all apartment URLs.")
        break
        driver.quit()
# Loop through the collected URLs and scrape details
for url in all_apartment_urls:
    scrape_apartment_details(url)

# Close the driver

