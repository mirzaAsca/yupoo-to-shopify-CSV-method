import json
import os

data_file = 'data.json'

if not os.path.exists(data_file):
    data = []

    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
