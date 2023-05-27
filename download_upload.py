import os
import requests
from bs4 import BeautifulSoup
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import re
from PIL import Image

def compress_image_if_necessary(file_path):
    img = Image.open(file_path)
    width, height = img.size
    megapixels = (width * height) / 1000000
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Get file size in MB

    print(f"Image {file_path} has a size of {file_size:.2f}MB and {megapixels:.2f}MP")

    if file_size > 1:
        print(f"Image {file_path} is larger than 1MB. Compressing...")
        img = img.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
        img.save(file_path, "JPEG", quality=90)
        print(f"Image {file_path} compressed successfully.")

    # Check if the image is 20MP or higher, and compress it further to a maximum of 15MP
    if megapixels >= 20:
        print(f"Image {file_path} is 20MP or higher. Compressing further to a maximum of 15MP...")
        scale_factor = (15 / megapixels) ** 0.5
        img = img.resize((int(width * scale_factor), int(height * scale_factor)), Image.ANTIALIAS)
        img.save(file_path, "JPEG", quality=90)
        print(f"Image {file_path} compressed further to a maximum of 15MP.")

def download_photos(session, url, product_names, album_main_links):
    headers = {'Referer': url}
    
    download_links = []
    for i, album_url in enumerate(album_main_links):

        folder_name = re.sub(r'[\\/:*?"<>|“”]', '-', product_names[i])
        output_folder = os.path.join("JIN-Photos", folder_name)
        folder_index = 1
        while os.path.exists(output_folder):
            output_folder = os.path.join("JIN-Photos", folder_name + f"({folder_index})")
            folder_index += 1
        os.makedirs(output_folder, exist_ok=True)

        response = session.get(album_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        img_tags = soup.find_all("img", attrs={"data-origin-src": True})
        links = []
        for j, img_tag in enumerate(reversed(img_tags)):
            photo_url = "https:" + img_tag["data-origin-src"]

            # Check if the file extension is PNG and skip it
            if photo_url.lower().endswith('.png'):
                print(f"Skipping PNG image {photo_url}")
                continue
            
            response = session.get(photo_url, headers=headers)
            file_path = os.path.join(output_folder, f"{j+1}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)

                compress_image_if_necessary(file_path)

            links.append(file_path)
            print(f"{file_path} downloaded successfully ")
        download_links.append(links)
    return download_links

def upload_photos(creds, album_main_links, product_names, folder_id):
    service = build('drive', 'v3', credentials=creds)
   
    google_links = []  # create an empty array to store the download links

    for i, album_url in enumerate(album_main_links):
        folder_name = re.sub(r'[\\/:*?"<>|“”]', '-', product_names[i])
        output_folder = os.path.join("JIN-Photos", folder_name)

        # Create a new folder with the same name as the local folder
        folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [folder_id]}
        folder = service.files().create(body=folder_metadata, fields='id').execute()

        # Upload the photos to the newly created folder
        new_folder_id = folder.get('id')
        for file_name in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file_name)
            file_metadata = {'name': file_name, 'parents': [new_folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Get the download link for the uploaded photo
            file_id = file.get('id')
            file = service.files().get(fileId=file_id, fields='webContentLink').execute()
            download_link = file.get('webContentLink')

            # Append the download link to the array
            google_links.append(download_link)

            print(f'{file_name} uploaded successfully. Download link: {download_link}')
    return google_links  # return the array of download links

