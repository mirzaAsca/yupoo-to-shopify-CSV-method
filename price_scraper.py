import requests
from bs4 import BeautifulSoup
import re


def scrape_prices(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    album_titles = soup.find_all("div", {"class": "text_overflow album__title"})

    prices = []

    for title in album_titles:
        text = title.text.strip()
        first_word = text.split()[0]
        first_price_match = re.search(r"\d+", first_word)
        if first_price_match:
            first_price = int(first_price_match.group() + "0")

            if 100 < first_price < 340:
                converted_price = round((first_price / 7.2) + 90)
            elif 340 <= first_price < 490:
                converted_price = round((first_price / 7.2) + 125)
            elif 490 <= first_price < 600:
                converted_price = round((first_price / 7.2) + 165)
            elif 600 <= first_price < 800:
                converted_price = round((first_price / 7.2) + 185)
            elif 800 <= first_price < 2000:
                converted_price = round((first_price / 7.2) + 210)

            increased_price = round(converted_price * 1.3)  # calculate increased price
            print("converted_price:", converted_price)
            print("increased_price:", increased_price)
            prices.append((converted_price, increased_price))
        else:
            prices.append(None)

    print("Response:", response)
    print("Extracted prices:", prices)

    return prices
