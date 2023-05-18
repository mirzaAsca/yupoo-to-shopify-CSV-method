import json

def replace_text_in_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Replace the unwanted text with a space
    for item in data:
        if "product_names" in item:
            item["product_names"] = item["product_names"].replace("\u201c\u201d", " ")

    # Save the modified data back to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Replace the path with the path to your data.json file
json_file_path = r"C:\Users\DT User\Desktop\projekti\selenium-photo\data.json"

replace_text_in_json_file(json_file_path)
