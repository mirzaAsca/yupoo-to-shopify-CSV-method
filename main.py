import json
import threading
from auth import authenticate
from name_scraper import scrape_names
from price_scraper import scrape_prices
from album_url_scraper import scrape_album_urls
from date_scraper import scrape_dates
from size_scraper import scrape_sizes
from download_upload import download_photos, upload_photos
import random
from csvmaker import create_csv
from config import url, folder_id
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


session = requests.Session()


def validate_and_load_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
    except Exception as e:
        print(f"Error while reading JSON file: {e}")

    return []


# Get the credentials
creds = authenticate()

# Create a lock for writing to the JSON file
json_lock = threading.Lock()


def scrape_page(url):
    # Scrape the names
    product_names = scrape_names(session, url)

    # Scrape the prices
    prices = scrape_prices(session, url)

    # Scrape the album URLs
    album_main_links = scrape_album_urls(session, url)

    # Load existing data from the JSON file
    data_file = "data.json"
    existing_data = validate_and_load_json(data_file)

    for i, album_url in enumerate(album_main_links):
        product_name = product_names[i]

        # Skip existing products
        if any(
            product.get("product_names") == product_name for product in existing_data
        ):
            continue
        if any(product.get("album_urls") == album_url for product in existing_data):
            continue

        # Skip products without a price
        if prices[i] is None:
            continue

        # Scrape the dates and sizes
        date_published, date_str = scrape_dates(session, album_url)
        sizes = scrape_sizes(session, album_url)

        # Download photos locally
        download_links = download_photos(session, url, [product_name], [album_url])
        # Upload photos to Google Drive and get links
        google_links = upload_photos(creds, [album_url], [product_name], folder_id)

        # Get the converted and increased prices
        converted_price, increased_price = prices[i]

        # Set the vendor based on the price
        if 100 <= converted_price <= 280:
            vendor = "Sneakers Republic"
        elif converted_price > 390:
            vendor = "Sneakers Republic Premium"
        else:
            vendor = ""

        # Generate 5 random digits
        random_numbers = "".join(random.choices("0123456789", k=5))

        # Store the data for the product
        product_data = {
            "Handle": product_name + "-" + random_numbers,
            "Title": product_name,
            "full_date_published": date_str,  # Add this line to store the full date format
            "Variant Price": converted_price,
            "Variant Compare At Price": increased_price,
            "Vendor": vendor,
            "album_urls": album_url,
            "date_published": date_published,
            "Option1 Value": sizes,
            "Image Src": google_links,
            "Tags": ["jin", date_published, album_url],
            "Image Alt Text": product_name,
            "SEO Description": product_name,
        }

        product_data["Handle"] = product_data["Handle"].replace(" ", "-")
        product_data["Image Alt Text"] = product_data["Image Alt Text"].replace(
            " ", "-"
        )

        # Append the new data to the existing data and save it to the JSON file
        with json_lock:
            existing_data = validate_and_load_json(data_file)
            existing_data.append(product_data)
            # Sort the data by the oldest date to the newest
            existing_data = sorted(
                existing_data,
                key=lambda x: x["date_published"]
                if x["date_published"] != "NA"
                else "999999",
            )
            with open(data_file, "w") as f:
                json.dump(existing_data, f, indent=2)

        # Debug statement
        with open(data_file, "r") as f:
            file_contents = f.read()

        print(f"JSON file content added: {product_data}")

        # Create the CSV file
        create_csv(existing_data)


def scrape_page_wrapper(page):
    current_url = f"{url}&page={page}"
    print(f"Scraping page {page}: {current_url}")
    scrape_page(current_url)


# Set the number of pages to scrape
num_pages_to_scrape = 10

# Create a ThreadPoolExecutor with a number of workers
with ThreadPoolExecutor(max_workers=2) as executor:
    # Submit the scraping tasks to the executor
    futures = [
        executor.submit(scrape_page_wrapper, page)
        for page in range(1, num_pages_to_scrape + 1)
    ]

    # Wait for all tasks to complete
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred while scraping: {e}")
