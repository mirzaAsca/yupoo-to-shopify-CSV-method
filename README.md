[![Watch DEMO on YouTube!](https://i.ibb.co/L1DdQks/Untitled.png)](https://www.youtube.com/watch?v=jWGo6DZl4ng "Watch DEMO on YouTube!")



# Project Documentation

## Overview

This project is specifically engineered to harvest product information from Yupoo Albums, where Chinese merchants showcase their products. It captures pertinent details, performs fundamental data processing, and subsequently saves the data individually or in structured arrays. After downloading and uploading to Google Drive, product photo links are conserved in a locally stored JSON file. Subsequently, a CSV file is generated based on this JSON data.

The data compiled is fully streamlined for Shopify's bulk import procedure using CSV files while simultaneously preserving the requisite structure for CSV bulk import. Various data elements are leveraged as tags for a Shopify store, thereby enhancing the store's maintainability, updates, and filtration processes. The tags associated with each product encompass a price tag, album URL tag, seller tag, and date tag. This tagging system simplifies product sorting, sourcing links for product orders, filtering products by sellers, and enables straightforward tracking, editing, or removal of outdated products.

The scraping procedure employs multithreading to simultaneously extract data from multiple Yupoo pages, thereby enhancing efficiency and speed.

### Importing Necessary Modules

Several custom modules are imported, including:

1. `auth`: Handles authentication to Google Drive API.
2. `name_scraper`, `price_scraper`, `album_url_scraper`, `date_scraper`, `size_scraper`: Various scrapers to retrieve product data.
3. `download_upload`: Contains functions for downloading product images and uploading them to Google Drive.
4. `csvmaker`: Functionality for creating CSV files from JSON data.
5. `config`: Stores configuration data like the base URL to scrape and Google Drive folder ID.

### Establishing a Session

A session is created with the `requests` library, to use it in subsequent web scraping tasks.

### Main Scraper Function: `scrape_page()`

This function accepts a URL and uses various scraper modules to collect product details such as names, prices, sizes, dates, and album URLs. It also checks if a product already exists in the existing dataset and if a product has a price. If the product is new and has a price, it downloads and uploads its photos, and processes the product data. The processed data is then appended to a local JSON file.

The function also generates CSV files from the updated JSON data.

### Multithreading with `ThreadPoolExecutor`

The script uses multithreading to scrape multiple pages simultaneously. The number of pages to scrape is controlled by the `num_pages_to_scrape` variable. The maximum number of threads to use is specified by the `max_workers` parameter in the `ThreadPoolExecutor`.

Each page to be scraped is submitted as a separate task to the executor, and the script waits for all tasks to complete before exiting.

## How to Run the Project

To run the script, simply execute the main Python file. The number of pages to scrape can be adjusted by changing the `num_pages_to_scrape` variable.

## Potential Issues

The script might encounter issues if a webpage doesn't contain the expected data or doesn't load correctly. In such cases, it may skip certain products or pages, and will print an error message to the console.

## Further Developments

The code could be extended to scrape additional data, handle more exceptions, or write data to different types of databases.

> **Note:** This documentation can be improved by contributing to this project. All contributions are welcomed!

# FEATURES FULL DESCRIPTION

## Custom Module `name_scraper`

This module performs several tasks as part of a product data scraping operation.

1. **Web Scraping**: Sends HTTP requests to a specified URL using the `requests` library and retrieves the page content.

2. **HTML Parsing**: Uses Beautiful Soup to parse the retrieved HTML content and searches for div elements containing product names.

3. **Text Processing**: Processes the retrieved product names to remove unnecessary whitespace, encode the text using UTF-8, remove non-ASCII and Chinese characters.

4. **Special Character Handling**: Replaces special characters not allowed in filenames (such as `\\/:*?"<>|`) with a dash (-).

5. **Fallback for Empty Names**: Assigns a default name ("sneaker" followed by a random number between 10000 and 99999) if a product name is empty after processing.

6. **Printing Results**: Prints each processed product name to the console for monitoring purposes.

7. **Return Value**: Returns a list of the processed product names.

## Custom Module `price_scraper`

The `scrape_prices` function in this custom module is designed to fetch and process the prices of products from a specific webpage. The core features of this function include:

1. **Price Extraction**: Scrapes the webpage and identifies the product prices using the Beautiful Soup library to parse the HTML content.

2. **Dynamic Price Conversion**: Converts the scraped prices into a new format through a set of predefined conversion rules. The conversion rules are based on the ranges of the original price.

3. **Increased Price Calculation**: Computes an increased price for each product based on the newly converted price, which is calculated as 130% of the converted price.

4. **Requests Integration**: Uses the `requests` library to manage HTTP requests and maintain the session with the website.

5. **Robust Error Handling**: Returns `None` when the price information for a product cannot be found or parsed correctly.

6. **Informative Console Outputs**: Prints out the fetched response, the converted prices, and the increased prices for debugging and transparency.

## Custom Module `album_url_scraper`

The `scrape_album_urls` function within the custom module performs the following core functionalities:

1. **Web Page Fetching**: It sends a GET request to the URL provided, and fetches the HTML content of the page.
2. **HTML Parsing**: Using Beautiful Soup, the fetched HTML is parsed to extract the required data.

3. **Album URL Scraping**: The function specifically targets and extracts all "album\_\_main" anchor tags from the parsed HTML. It then constructs the absolute URLs for these albums (taking into account the base URL of the provided page) and appends a specific query parameter (`?uid=1`) to each URL.

4. **URL Aggregation**: All album URLs are gathered and returned in a list.

5. **URL Logging**: The function prints each constructed URL for tracking purposes.

## Custom Module `date_scraper`

The `scrape_dates` custom module provides the following core features:

1. **Date Scraping**: The module extracts the date published from a given album URL. It makes use of the `requests` library to send an HTTP GET request and retrieve the webpage content. The `BeautifulSoup` library is then used to parse the HTML content and find the specific element containing the date information.

2. **Date Formatting**: The scraped date is processed and formatted into a standardized format. The module removes any dashes from the date string, extracts the year and month, and generates a formatted `date_published` value in the format "YYMM" (e.g., 2305 for May 2023).

3. **Error Handling**: If the module is unable to find the date element on the webpage, it returns "NA" as the `date_published` value, indicating that the date is not available. The module also prints relevant debug messages for troubleshooting purposes.

These features enable the extraction and formatting of date information from a webpage, allowing for further processing and analysis.

## Custom Module `size_scraper`

The custom module provides the following core features:

1. **Scraping Sizes**: The `scrape_sizes` function is designed to scrape the available sizes for a product from a given album URL. It uses the `requests` library to retrieve the HTML content of the page and `BeautifulSoup` for parsing and extracting the relevant information.

2. **Parsing Size Information**: The function extracts size information from the HTML content using regular expressions (`re`). It searches for numeric values or size ranges in the text and returns an array of sizes.

3. **Handling Size Ranges**: If the size information is not found directly, the function looks for size ranges (e.g., "5-10" or "5/10") and generates a list of sizes within that range. The start and end values are extracted using regular expressions.

4. **Filtering Sizes**: The function filters the extracted sizes based on a predefined range (35 to 47) to remove irrelevant or out-of-range values.

5. **Generating Size List**: If there are only two sizes in the filtered list, the function generates a complete list of sizes within that range. For example, if the filtered list is [40, 42], the function will return [40, 41, 42].

6. **Returning Sizes**: The function returns the final list of sizes or "N/A" if no sizes were found or extracted successfully.

These features allow for efficient extraction and processing of size information from the provided album URL, making it easier to analyze and work with product size data.

## Custom Module `download_upload`

The custom module contains functions related to image processing, downloading photos, and uploading photos to Google Drive. The core features of this module are:

1. **Image Compression:** The `compress_image_if_necessary()` function takes a file path as input and checks if the image size exceeds 1MB. If it does, the image is resized and compressed to reduce its file size. Additionally, if the image has a resolution of 20 megapixels or higher, it is further compressed to a maximum of 15 megapixels.

2. **Photo Downloading:** The `download_photos()` function downloads photos from a given album URL. It takes a session object, the URL of the webpage, product names, and album URLs as input. The function parses the webpage, extracts image tags, and downloads the corresponding photos. The downloaded photos are saved in a local folder with the product name as the folder name. The function also calls the `compress_image_if_necessary()` function to compress the downloaded images if necessary. It returns a list of download links for the downloaded photos.

3. **Photo Uploading to Google Drive:** The `upload_photos()` function uploads photos to a specified folder on Google Drive. It takes Google Drive credentials, album URLs, product names, and a folder ID as input. The function uses the Google Drive API to authenticate and create a new folder with the product name. It then uploads the photos from the local folder to the newly created folder on Google Drive. After uploading each photo, it retrieves the download link for the uploaded photo and appends it to an array. The function returns an array of download links for the uploaded photos.

These features provide functionality for image processing, downloading photos, and uploading photos to Google Drive, which can be useful for various applications involving image manipulation and storage.

## Custom Module `csvmaker`

The core features of the `create_csv` custom module are as follows:

1. **Creating a CSV File**: The module creates a CSV file named "jin.csv" to store the product data.
2. **Sorting Data**: The data is sorted by the oldest date to the newest using the `full_date_published` field.
3. **Writing Headers**: The module writes the header row in the CSV file, containing various column names.
4. **Writing Rows**: The module iterates over the provided data and writes each item as a row in the CSV file.
5. **Handling Missing Data**: The module handles cases where certain fields in the data are missing or have different lengths. It ensures that the row structure is maintained.
6. **Mapping Data to Columns**: The module maps the corresponding data fields to their respective columns in the CSV file.
7. **Adding Additional Header**: The module adds an extra column header named "Full Date" to store the full date information.
8. **Populating Rows**: The module populates the rows with the relevant data, including images, options, variant information, and the full date.

This custom module is used to convert the collected product data into a CSV format, which can be easily opened and analyzed using spreadsheet software.
