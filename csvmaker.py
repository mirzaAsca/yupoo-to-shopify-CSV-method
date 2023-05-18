import json
import csv

def create_csv(data):
    # Sort the data by the oldest date to the newest
    data = sorted(data, key=lambda x: x['full_date_published'] if x['full_date_published'] != "NA" else "99999999")
    # Create a CSV file
    with open("jin.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        header = [
            "Handle",
            "Title",
            "Vendor",
            "Tags",
            "Image Alt Text",
            "SEO Description",
            "Product Category",
            "Type",
            "Published",
            "Option1 Name",
            "Status",
            "Image Src",
            "Image Position",
            "Option1 Value",
            "Variant Inventory Policy",
            "Variant Fulfillment Service",
            "Variant Price",
            "Variant Compare at Price",
            "Full Date" # New header column added
        ]
        writer.writerow(header)

        # Write rows
        for item in data:
            base_row = [
                item["Handle"],
                item["Title"],
                item["Vendor"],
                ",".join(item["Tags"]),
                item["Image Alt Text"],
                item["SEO Description"],
                "Apparel & Accessories > Shoes",
                "Sneakers",
                "TRUE",
                "size",
                "active",
            ]

            image_src_len = len(item["Image Src"])
            option_value_len = len(item["Option1 Value"])
            max_len = max(image_src_len, option_value_len)

            for index in range(max_len):
                row = []

                if index < image_src_len:
                    image_src = item["Image Src"][index]
                    image_position = index + 1
                else:
                    image_src = ""
                    image_position = ""

                if index < option_value_len:
                    option_value = item["Option1 Value"][index]
                    variant_inventory_policy = "deny"
                    variant_fulfillment_service = "manual"
                    variant_price = item["Variant Price"]
                    variant_compare_at_price = item["Variant Compare At Price"]
                else:
                    option_value = ""
                    variant_inventory_policy = ""
                    variant_fulfillment_service = ""
                    variant_price = ""
                    variant_compare_at_price = ""

                if index == 0:
                    row = base_row + [image_src, image_position, option_value, variant_inventory_policy, variant_fulfillment_service, variant_price, variant_compare_at_price, item["full_date_published"]] # Map "Full Date" to date_str
                else:
                    row = [item["Handle"]] + [""] * (len(base_row) - 1) + [image_src, image_position, option_value, variant_inventory_policy, variant_fulfillment_service, variant_price, variant_compare_at_price, ""]

                writer.writerow(row)
