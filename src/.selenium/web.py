from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = 'https://www.immobilier.ch/fr/louer/appartement/geneve/geneve/pilet-renaud-locations-residentielles-41/studio-meuble-attique-centre-ville-998907'

# Open the URL
driver.get(url)

# Wait for the dynamic content to load
time.sleep(5) # Adjust this time based on your internet speed

# Get the page source and parse it
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Get the first apartment listing
apartment = soup.find('div', class_='filter-item-container')

# Extract details
price = apartment.find('strong', class_='title').text.strip() if apartment.find('strong', class_='title') else 'No price'
apartment_type = apartment.find('p', class_='object-type').text.strip() if apartment.find('p', class_='object-type') else 'No type'
location = apartment.find_all('p')[1].text.strip() if len(apartment.find_all('p')) > 1 else 'No location'

# Print the extracted details
print(f'Price: {price}\nApartment Type: {apartment_type}\nLocation: {location}')

# Close the browser
driver.quit()
