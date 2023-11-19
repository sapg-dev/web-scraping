from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
# Set up the Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)




main_page_url = 'https://www.immobilier.ch/fr/louer/appartement-maison/geneve/geneve/page-1?t=rent&c=1;2&p=c10377&pn=8000&nb=false'

# Navigate to the main page
driver.get(main_page_url)

# Find an apartment listing in the "Location" category and click on it
apartment_links = driver.find_elements_by_css_selector('a[category="Location"]')
if apartment_links:
    apartment_links[0].click()  # Click on the first apartment in the list
    time.sleep(5)  # Wait for the apartment page to load
# URL of the individual apartment listing
url = 'https://www.immobilier.ch/fr/louer/appartement/geneve/geneve/nsr-group-1607/magnifique-appartement-vue-parc-bertrand-999481'

# Open the URL
driver.get(url)

# Wait for the dynamic content to load
time.sleep(5)  # Adjust this time based on your internet speed

# Get the page source and parse it
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract details
address_elements = driver.find_elements(By.CLASS_NAME, 'object-address')
price_element = driver.find_element(By.CLASS_NAME, 'im__postDetails__price')
price_text = price_element.text
price_numeric = int(''.join(filter(str.isdigit, price_text)))


addresses = [element.text for element in address_elements]

match = re.search(r'(\d+)$', url)
if match:
    apartment_id = match.group(1)
else:
    apartment_id = None
apartment_id = apartment_id

# Construct the XPath for the "Read More" button using the extracted apartment ID
button_xpath = f'//a[contains(@href, "javascript:sDetail.readMore({apartment_id})")]'

# Wait for the "Read More" button to become clickable
try:
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    )
    button.click()

    # Explicit wait for the table to load
    # You can adjust the timeout as needed

    # Find the specific list items using the refined CSS selector
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".im__table.im__table--responsive.im__row .im__table__row.js-last-col .im__assets__title.im__assets__title--big"))
    )
except NoSuchElementException as e:
    print(f"Element not found: {e}")

# Explicit wait for the table to load
# You can adjust the timeout as needed

# Find the specific list items using the refined CSS selector
elements = driver.find_elements(By.CSS_SELECTOR, ".im__table.im__table--responsive.im__row .im__table__row.js-last-col .im__assets__title.im__assets__title--big")


# Get the textual content of the element without HTML tags
description_element = driver.find_element(By.CLASS_NAME, 'im__postContent__body')
description_text = description_element.text

# Create the apartment_data dictionary


# Convert the dictionary to a JSON string


# Print the JSON data


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

# Print or process the image URLs
apartment_details = {
    'price': price_numeric,
    'addresses': addresses,
    'description': description_text,
    'elements': [element.text for element in elements],
    'url': image_urls
}

# Nesting the apartment_details under 'apartment'
apartment_data = {'apartment': apartment_details}

# Convert the dictionary to a JSON string
json_data = json.dumps(apartment_data, indent=4)

# Print the JSON data
print(json_data)

# Write JSON data to a file named 'estate.json'
with open('estate.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

print("JSON data has been saved to estate.json")

# Close the browser
driver.quit()
