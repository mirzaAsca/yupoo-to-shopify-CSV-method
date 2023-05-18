import requests
from bs4 import BeautifulSoup
import re

def scrape_sizes(session, album_url):
    response = session.get(album_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    size_elem = soup.find('div', {'class': 'showalbumheader__gallerysubtitle htmlwrap__main'})
    size_text = size_elem.text
    size_array = re.findall(r'\d+(?:\.\d+)?', size_text)

    if not size_array:
        size_range = re.findall(r'\d+(?:\.\d+)?[-/]\d+(?:\.\d+)?', size_text)
        if size_range:
            start, end = re.findall(r'\d+(?:\.\d+)?', size_range[0])
            size_array = [str(x) for x in range(int(float(start)), int(float(end))+1)]

    if not size_array:
        return "N/A"
    else:
        sizes = [float(x) for x in size_array]
        sizes = [x for x in sizes if x >= 35 and x <= 47]

        if len(sizes) == 2:
            new_sizes = []
            for i in range(int(sizes[0]), int(sizes[1])+1):
                new_sizes.append(i)
            sizes = new_sizes

        return sizes
