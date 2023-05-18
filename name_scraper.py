import requests
from bs4 import BeautifulSoup
import re
import random

def scrape_names(session,url):
    
    response = session.get(url)

    # Scrape the product name
    product_names = []

    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    album_spaces = soup.find_all('div', {'class': 'text_overflow album__title'})
    for space in album_spaces:
        # Encode the text using utf-8 before manipulating it
        text = space.text.strip().encode('utf-8')
        # Remove any non-ASCII characters
        text = text.decode('ascii', 'ignore')
        # Remove Chinese characters
        text = re.sub('[\u4e00-\u9fff]+', '', text).replace('"', '')
        # Remove the first word from the text
        text = " ".join(text.split()[1:])
        if not text:
            text = f"sneaker{random.randint(10000, 99999)}"

        # Apply the same formatting logic for folder_name
        formatted_product_name = re.sub(r'[\\/:*?"<>|]', '-', text)
        
        product_names.append(formatted_product_name)
        print(formatted_product_name)

    return product_names

