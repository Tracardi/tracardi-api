# How to import data with python?

You can use `/track` endpoint to import data form CSV.

Example:

```python
import csv
import requests


def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        for row in reader:  # Iterate over the remaining rows
            yield dict(zip(headers, row))  # spit out column name and data


# Provide the path to your CSV file
config = ('file1.csv', 'phone-calls', 'id')
# config = ('file2.csv', 'sms-send', 'id')

source_id = "c437d599-5d38-43e2-84b9-c6267dce6410"

for row in read_csv(config[0]):

    payload = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": row[config[2]]
        },
        "events": [
            {
                "type": config[1],
                "properties": row
            }
        ]
    }

    response = requests.post(url="http://localhost:8686/track", json=payload)
    
    # Display response
    print(response.content)
```


---
This document also answers the questions:
- How to programmatically import data to Tracardi?
- Is there a way to use code to import data to Tracardi?
- How to use API to import data?