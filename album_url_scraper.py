import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit


def scrape_album_urls(session, url):
    response = session.get(url)
    album_urls = []
    album_main_links = []
    soup = BeautifulSoup(response.content, 'html.parser')
    album_main_tags = soup.find_all("a", class_="album__main")

    # Extract the base URL from the given url
    parsed_url = urlsplit(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for album_main in album_main_tags:
        album_url = base_url + album_main["href"] + "?uid=1"
        album_main_links.append(album_url)
        print("Product URL:", album_url)

    return album_main_links
