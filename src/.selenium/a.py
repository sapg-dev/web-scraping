
import re
url = 'https://www.immobilier.ch/fr/louer/appartement/geneve/geneve/pilet-renaud-locations-residentielles-41/studio-meuble-attique-centre-ville-998907'

# Use regular expression to extract the apartment ID
match = re.search(r'(\d+)$', url)
if match:
    apartment_id = match.group(1)
else:
    apartment_id = None

print(f"Apartment ID: {apartment_id}")