import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def scrape_hero_data():
    # URL of the Dota 2 heroes page
    url = "https://www.dotafire.com/dota-2/heroes"

    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all hero elements on the page
    hero_elements = soup.find_all('a', class_='hero-list__item')

    # List to store hero data
    heroes = []
    # Loop through each hero element and extract the name and image
    for hero in hero_elements:
        hero_name = hero.find('div', class_='hero-name').text.strip()
        img_tag = hero.find('img')
        img_url = "https://www.dotafire.com" + img_tag['src']
        hero_data = {
            'name': hero_name,
            'image_url': img_url
        }
        heroes.append(hero_data)
    
    return heroes

def download_hero_images(heroes):
    if not os.path.exists('heroes'):
        os.makedirs('heroes')
    
    for hero in heroes:
        response = requests.get(hero['image_url'])
        img = Image.open(BytesIO(response.content))
        img.save(f"heroes/{hero['name'].replace(' ', '-').lower()}.png")

if __name__ == "__main__":
    heroes = scrape_hero_data()
    download_hero_images(heroes)


# for hero in heroes:
#     print(f"Hero Name: {hero['name']}, Image URL: {hero['image_url']}")
