import requests
import json

# STORE INFORMATIONS
SHOP_NAME = 'republic-of-collections'
ACCESS_TOKEN = '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'
FILE_NAME = 'sample_products.jsonl'

# Set up headers and endpoint URL
headers = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': ACCESS_TOKEN
}
url = f'https://{SHOP_NAME}.myshopify.com/admin/api/2022-01/graphql.json'

# Step 1: Reserve a link for the JSONL file
mutation = '''
mutation {
    stagedUploadsCreate(input: {
        resource: BULK_MUTATION_VARIABLES,
        filename: "sample_products",
        mimeType: "text/jsonl",
        httpMethod: POST
    }) {
        userErrors {
            field,
            message
        }
        stagedTargets {
            url
            resourceUrl
            parameters {
                name,
                value
            }
        }
    }
}
'''

response = requests.post(url, json={'query': mutation}, headers=headers)
response_data = json.loads(response.text)
print("stagedUploadsCreate response:", response.text)

# Extract stagedTargets and parameters from the response
staged_targets = response_data['data']['stagedUploadsCreate']['stagedTargets'][0]
parameters = {param['name']: param['value'] for param in staged_targets['parameters']}
resource_url = staged_targets['resourceUrl']
key_param = next(param for param in staged_targets['parameters'] if param['name'] == 'key')
print("The value of the key:", key_param['value'])


# Set the upload URL and parameters
upload_url = staged_targets['url']
upload_parameters = {
    **parameters,
    "acl": "private",
    "Content-Type": "text/jsonl",
    "success_action_status": "201",
}

# Set the path to your JSONL file
jsonl_file_path = "C://Users//DT User//Desktop//projekti//selenium-photo//CHUANQII-JIN-SCRAPER//sample_products.jsonl"

# Open the JSONL file in binary mode
with open(jsonl_file_path, "rb") as jsonl_file:
    # Add the file to the upload parameters
    upload_parameters["file"] = jsonl_file

    # Send the POST request to the staged upload URL with the JSONL data
    response = requests.post(upload_url, files=upload_parameters)

# Check if the upload was successful
if response.status_code == 201:
    print("File uploaded successfully")
else:
    print("File upload failed")
    print("")

staged_upload_path = key_param['value']

mutation = """
mutation {
  bulkOperationRunMutation(
    mutation: "mutation call($input: ProductInput!) { productCreate(input: $input) { product {id title variants(first: 10) {edges {node {id title inventoryQuantity }}}} userErrors { message field } } }",
    stagedUploadPath: "{staged_upload_path}") {
    bulkOperation {
      id
      url
      status
    }
    userErrors {
      message
      field
    }
  }
}
"""

mutation = mutation.replace("{staged_upload_path}", staged_upload_path)
response = requests.post(url, json={'query': mutation}, headers=headers)
response_data = json.loads(response.text)
print("bulkOperationRunMutation response:", response.text)


webhook_subscription_mutation = '''
mutation {
    webhookSubscriptionCreate(
        topic: BULK_OPERATIONS_FINISH,
        webhookSubscription: {
            format: JSON,
            callbackUrl: "https://692c-92-36-185-66.eu.ngrok.io/webhook"
        }
    ) {
        userErrors {
            field,
            message
        }
        webhookSubscription {
            id
        }
    }
}
'''

response = requests.post(url, json={'query': webhook_subscription_mutation}, headers=headers)
response_data = json.loads(response.text)
print("webhookSubscriptionCreate response:", response.text)
 