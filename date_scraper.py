import requests
from bs4 import BeautifulSoup


def scrape_dates(session, album_url):
    response = session.get(album_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    date_elem = soup.find('time', {'class': 'text_overflow'})
    if date_elem:
        date_str = date_elem.text.strip()
        date_str = date_str.replace('-', '')
        year = date_str[:4]
        month = date_str[4:6]
        date_published = year[2:] + month
        print("date published:", date_published)
        return date_published, date_str  # Return both date_published and date_str
    else:
        print("date published: NA")
        return "NA", "NA"  # Return both date_published and date_str as "NA"