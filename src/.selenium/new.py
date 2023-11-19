import json
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

# Set up the Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def scrape_apartment_details(url):
    try:
        # Open the URL
        driver.get(url)

        # Wait for the dynamic content to load
        time.sleep(10)  # Adjust this time based on your internet speed

        # Extract details
        address_elements = driver.find_elements(By.CLASS_NAME, 'object-address')
        price_element = driver.find_element(By.CLASS_NAME, 'im__postDetails__price')
        price_text = price_element.text
        ## price_numeric = int(''.join(filter(str.isdigit, price_text)))
        split_price_text = price_text.split("CHF")
        if len(split_price_text) > 1:
            # Assuming the first part after splitting contains the monthly rent
            monthly_rent_text = split_price_text[1].split('/')[0]  # Get the part before "/mois"
            # Remove non-digit characters like thousand separators and currency symbols
            monthly_rent_text = monthly_rent_text.replace("'", "").replace(".", "").strip()
            price_numeric = int(''.join(filter(str.isdigit, monthly_rent_text)))
        else:
            price_numeric = None  # or some default value or handling

        addresses = [element.text for element in address_elements]

        match = re.search(r'(\d+)$', url)
        if match:
            apartment_id = match.group(1)
        else:
            apartment_id = None
        apartment_id = apartment_id

        # Construct the XPath for the "Read More" button using the extracted apartment ID
        button_xpath = f'//a[contains(@href, "javascript:sDetail.readMore({apartment_id})")]'

        # Check if the "Read More" button exists
        button_elements = driver.find_elements(By.XPATH, button_xpath)
        if button_elements:
            # If the button exists, wait for it to become clickable and then click it
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                button.click()
                print("Read More button clicked.")
            except TimeoutException as e:
                print(f"Timeout waiting for element: {e}")
        else:
            print("Read More button not found.")

            # Explicit wait for the table to load, if necessary
            # You can adjust the timeout as needed
        try:
                # Find the specific list items using the refined CSS selector
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".im__table.im__table--responsive.im__row .im__table__row.js-last-col .im__assets__title.im__assets__title--big"))
                )
        except TimeoutException as e:
                print(f"Timeout waiting for table elements: {e}")
                elements = []

# [Continue with the rest of your existing code]


        # Get the textual content of the element without HTML tags
        description_element = driver.find_element(By.CLASS_NAME, 'im__postContent__body')
        description_text = description_element.text

        # Extract image URLs
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.im__banner__slide img')

        # URL to exclude
        exclude_url = "https://www.immobilier.ch/Images/Loading/Detail.jpg?v=2"

        # Extract URLs, ensuring uniqueness and excluding the specific URL
        image_urls_set = set()
        for img in image_elements:
            # Check if 'data-lazy' attribute exists
            lazy_load_url = img.get_attribute('data-lazy')
            if lazy_load_url:
                if lazy_load_url != exclude_url and lazy_load_url not in image_urls_set:
                    image_urls_set.add(lazy_load_url)
            else:
                src_url = img.get_attribute('src')
                if src_url and src_url != exclude_url and src_url not in image_urls_set:
                    image_urls_set.add(src_url)

        # Convert the set to a list for further processing if necessary
        image_urls = list(image_urls_set)

        # Create the apartment_details dictionary
        apartment_details = {
            'price': price_numeric,
            'addresses': addresses,
            'description': description_text,
            'elements': [element.text for element in elements],
            'url': image_urls
        }

        # Check if the JSON file 'estate.json' exists
        if os.path.exists('estate.json'):
            # If it exists, load the existing JSON data
            with open('estate.json', 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                
        else:
            # If the JSON file doesn't exist, create an empty list
            existing_data = []

        # Append the new apartment details to the existing list or create a new list if empty
        existing_data.append({'apartment': apartment_details})
        print(json.dumps(apartment_details, indent=4))

        # Write the updated data back to the JSON file
        with open('estate.json', 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4)

        # Print the JSON data
        

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
