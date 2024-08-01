# Importing Data to Tracardi Documentation

## Introduction

This documentation outlines the steps to import data into Tracardi, a data management platform that stores data in
Elasticsearch. 

## Methods for Data Import into Tracardi

There are multiple methods available for importing data into Tracardi:

1. **Simple Import Script:** The most flexible and recommended approach by Tracardi is to use a custom import script to
   transfer your data. This method allows you to have full control over the import process.

2. **Tracardi's Built-in Import Feature:** Tracardi also provides its own built-in import feature. This option is
   user-friendly and can be utilized for importing data directly within the Tracardi platform.

3. **Elasticsearch and Kibana Integration:** If preferred, you can leverage Elasticsearch's internal mechanisms and the
   powerful data visualization capabilities of Kibana. Here is a resource guide on how to import data into Elasticsearch
   using File Data
   Visualizer: [Elastic Blog - Importing CSV and Log Data into Elasticsearch with File Data Visualizer](https://www.elastic.co/blog/importing-csv-and-log-data-into-elasticsearch-with-file-data-visualizer).

## Types of Objects in Tracardi

Tracardi allows you to work with three primary types of objects: profiles, sessions, and events. This
guide will help you get started with the data import process.

1. **Profiles:** Profiles represent individual entities, such as customers or users. In most cases, you'll need to
   import profile objects when you start working with Tracardi.

2. **Sessions:** Sessions correspond to user sessions or interactions, capturing the behavior and engagement of your
   users over time. You may choose to import session objects in addition to profiles if you want to track user
   interactions.

3. **Events:** Events are specific actions or occurrences, such as a user making a purchase or clicking on a link.
   Importing events is necessary when you want to capture detailed user actions and their timestamps.

## Steps to Start Importing Data

Follow these steps to begin the process of importing data into Tracardi:

1. **Find the Data:** Locate the data that you intend to import into Tracardi. This data can be sourced from various
   platforms or sources.

2. **Find the Data Schema in Tracardi:** Understand the structure of the data you plan to import by finding the relevant
   schema within Tracardi. You can do this by using a test section in Tracardi to register a single event, which will
   automatically generate a profile, session, and event. You can access the schema for each object by following these
   steps:

    - Click on the "3 dots" icon near each object (profile, session, or event).
    - Navigate to the JSON tab to access the schema for the respective object.

3. **Prepare Mapping:** Before importing data, prepare a mapping that aligns the fields in your data source with the
   schema in Tracardi. This mapping will help ensure that your data is accurately ingested.

4. **Write a Simple Script:** Create a script in your preferred programming language that extracts data from your source
   and imports it into Tracardi using the prepared mapping. This script should establish a connection to Tracardi's
   Elasticsearch database for data insertion.

5. **Run the Script:** Execute the script to begin the data import process. The script will transfer your data into
   Tracardi, where it will be stored in Elasticsearch.

## Tracardi Data Structure

The structure for each object (profile, session, and event) in Tracardi can be found within the platform itself. To
access the schema for each object, use the following steps:

1. Create a test section in Tracardi to register a single event, which will generate a profile, session, and event.
2. Click on the "3 dots" icon near the object you are interested in (profile, session, or event).
3. Navigate to the JSON tab, where you will find the schema for the selected object.

## Examples

Here are examples of each object in Tracardi:

=== "Profile Object Schema"
```json
{
  "id": "cc89f945-5262-4859-b8f7-4eebe3d740ba",
  "ids": [
    "cc89f945-5262-4859-b8f7-4eebe3d740ba"
  ],
  "metadata": {
    "time": {
      "insert": "2023-10-16T09:25:14.336120",
      "create": null,
      "update": "2023-10-16T09:25:21.396452",
      "segmentation": null,
      "visit": {
        "last": null,
        "current": "2023-10-16T09:25:14.342063",
        "count": 1,
        "tz": "Europe/Sarajevo"
      }
    },
    "aux": {},
    "status": null
  },
  "stats": {
    "visits": 0,
    "views": 0,
    "counters": {}
  },
  "traits": {},
  "segments": [],
  "interests": {},
  "consents": {
    "cookies": {
      "revoke": null
    }
  },
  "active": true,
  "aux": {
    "geo": {
      "continent": "Europe"
    }
  },
  "data": {
    "pii": {
      "firstname": "Maria",
      "lastname": "White",
      "name": "Maria White",
      "birthday": "1986-01-22T04:51:59",
      "language": {
        "native": null,
        "spoken": null
      },
      "gender": "female",
      "education": {
        "level": "Technical Education"
      },
      "civil": {
        "status": "Married"
      },
      "attributes": {
        "height": 176,
        "weight": 65,
        "shoe_number": 44
      }
    },
    "contact": {
      "email": "powen@example.org",
      "phone": null,
      "app": {
        "whatsapp": "980-060-6463x2839",
        "discord": null,
        "slack": "@White",
        "twitter": "@tracardi",
        "telegram": "@Maria",
        "wechat": null,
        "viber": null,
        "signal": null,
        "other": {}
      },
      "address": {
        "town": "Blakeberg",
        "county": null,
        "country": "Libyan Arab Jamahiriya",
        "postcode": "61402",
        "street": "417 Randy Mall",
        "other": null
      },
      "confirmations": []
    },
    "identifier": {
      "id": null,
      "badge": null,
      "passport": null,
      "credit_card": null,
      "token": null,
      "coupons": null
    },
    "devices": {
      "names": [],
      "last": {
        "geo": {
          "country": {
            "name": "Asia/Shanghai",
            "code": "CN"
          },
          "city": "Sishui",
          "county": "CN",
          "postal": null,
          "latitude": 35.64889,
          "longitude": 117.27583
        }
      }
    },
    "media": {
      "image": "http://tracardi.com/demo/image/female/profile_8.JPG",
      "webpage": "http://www.tracardi.com",
      "social": {
        "twitter": "@tracardi",
        "facebook": "tracardi",
        "youtube": "@mytag",
        "instagram": null,
        "tiktok": null,
        "linkedin": null,
        "reddit": null,
        "other": {}
      }
    },
    "preferences": {
      "purchases": [],
      "colors": [
        "gray"
      ],
      "sizes": [
        "xxl"
      ],
      "devices": [
        "tablet"
      ],
      "channels": [
        "direct"
      ],
      "payments": [
        "cash"
      ],
      "brands": [
        "Maybelline"
      ],
      "fragrances": [
        "Chanel No. 5"
      ],
      "services": [
        "Insurance"
      ],
      "other": []
    },
    "job": {
      "position": "Customer Service Representative",
      "salary": 3521,
      "type": null,
      "company": {
        "name": "Target",
        "size": 16,
        "segment": "Healthcare",
        "country": "Switzerland"
      },
      "department": "Design"
    },
    "metrics": {
      "ltv": 0,
      "ltcosc": 0,
      "ltcocc": 0,
      "ltcop": 0,
      "ltcosv": 0,
      "ltcocv": 0,
      "next": null,
      "custom": {}
    },
    "loyalty": {
      "codes": [
        "but1get2"
      ],
      "card": {
        "id": null,
        "name": null,
        "issuer": "Champion",
        "expires": "2024-01-31T23:51:46",
        "points": 40
      }
    }
  }
}
```
=== "Session Object Schema"
```json
{
   "id": "e4b1e0b0-d90d-4cd0-86c3-9c91ccab25af",
   "metadata": {
      "time": {
         "insert": "2023-10-16T09:24:30.292701",
         "update": null,
         "timestamp": 1697448270.292705,
         "duration": 0,
         "weekday": 0
      },
      "channel": "Internal",
      "aux": {},
      "status": "active"
   },
   "profile": {
      "id": "44f12a8c-bdc9-44a4-bf19-bbc1d0a4ccd8"
   },
   "device": {
      "name": "Other",
      "brand": "LG",
      "model": "Degree",
      "type": null,
      "touch": false,
      "ip": null,
      "resolution": null,
      "geo": {
         "country": {
            "name": "America/Havana",
            "code": "CU"
         },
         "city": "Varadero",
         "county": "CU",
         "postal": null,
         "latitude": 23.15678,
         "longitude": -81.24441
      },
      "color_depth": null,
      "orientation": null
   },
   "os": {
      "name": "Android",
      "version": "4.2.2"
   },
   "app": {
      "type": null,
      "name": null,
      "version": null,
      "language": "sc_IT",
      "bot": false,
      "resolution": null
   },
   "utm": {
      "source": null,
      "medium": null,
      "campaign": null,
      "term": null,
      "content": null
   },
   "context": {
      "time": {
         "local": "8/26/2021, 9:36:13 PM",
         "tz": "Asia/Katmandu"
      },
      "location": {
         "country": {
            "name": "America/Havana",
            "code": "CU"
         },
         "city": "Varadero",
         "county": "CU",
         "postal": null,
         "latitude": "23.15678",
         "longitude": "-81.24441"
      },
      "device": {
         "name": "Other",
         "brand": "Werner-White",
         "model": "degree company knowledge",
         "type": "tablet",
         "touch": false,
         "ip": null,
         "resolution": "1280x960",
         "geo": {
            "country": {
               "name": "America/Havana",
               "code": "CU"
            },
            "city": "Varadero",
            "county": "CU",
            "postal": null,
            "latitude": "23.15678",
            "longitude": "-81.24441"
         },
         "color_depth": 8,
         "orientation": "landscape-primary"
      },
      "os": {
         "name": "macOS",
         "version": "21.04"
      },
      "app": {
         "type": "mobile_browser",
         "name": "Internet Explorer",
         "version": "50.0",
         "language": "ja-JP",
         "bot": false,
         "resolution": "3840x1080"
      },
      "page": {
         "url": "https://dixon.com/wp-content/blog/wp-content/post.html",
         "path": "/wp-content/blog/wp-content/post.html",
         "hash": "",
         "title": "Rubber Shirt",
         "referer": {
            "host": "https://dixon.com",
            "query": null
         },
         "history": {
            "length": 6
         }
      },
      "browser": {
         "local": {
            "browser": {
               "name": "Netscape",
               "engine": "Gecko",
               "appVersion": "5.0 (X11)",
               "userAgent": "Mozilla/5.0 (Linux; Android 4.2.2) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/49.0.842.0 Safari/531.0",
               "language": "sc_IT",
               "onLine": true,
               "javaEnabled": false,
               "cookieEnabled": true
            },
            "device": {
               "platform": "Android 2.3.6"
            }
         }
      },
      "storage": {
         "local": {
            "__anon_id": "\"f30ee0a4-be4e-4571-97b2-80b32a18a77f\"",
            "profileQuery": "",
            "eventQuery": "",
            "sessionQuery": ""
         },
         "cookie": {
            "cookies1": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22f573ac77-2d68-41f1-b768-d2d4aa986382%22",
            "cookies2": "tracardi-session-id=fb151f11-e6f4-4cbf-9ad9-39414c1219f8, ajs_user_id=null, ajs_group_id=null, ajs_anonymous_id=\"f573ac77-2d68-41f1-b768-d2d4aa986382\""
         }
      },
      "screen": {
         "width": 2379,
         "height": 819,
         "innerWidth": 1507,
         "innerHeight": 964,
         "availWidth": 1526,
         "availHeight": 956,
         "colorDepth": 24,
         "pixelDepth": 24
      },
      "ip": "0.0.0.0"
   },
   "properties": {},
   "traits": {},
   "aux": {}
}

```

=== "Event Object Schema"
```json
 {
   "id": "053a1536-167d-4f1f-b066-2d556274a261",
   "name": "Test Event",
   "type": "test-event",
   "metadata": {
      "aux": {},
      "time": {
         "insert": "2023-08-16T08:55:00.055083",
         "create": null,
         "update": null,
         "process_time": 0.02,
         "total_time": 0
      },
      "ip": null,
      "status": "collected",
      "channel": null,
      "processed_by": {
         "rules": [],
         "flows": [],
         "third_party": []
      },
      "profile_less": false,
      "debug": false,
      "valid": true,
      "error": false,
      "warning": false,
      "merge": false,
      "instance": null
   },
   "utm": {
      "source": null,
      "medium": null,
      "campaign": null,
      "term": null,
      "content": null
   },
   "properties": {},
   "traits": {},
   "source": {
      "id": "1"
   },
   "session": {
      "id": "1",
      "start": "2023-10-16T08:54:59.956772",
      "duration": 0,
      "tz": "utc"
   },
   "profile": null,
   "context": {},
   "request": {},
   "config": {},
   "tags": {
      "values": [],
      "count": 0
   },
   "aux": {},
   "device": {},
   "os": {},
   "app": {},
   "hit": {},
   "data": {},
   "journey": {
      "state": null
   }
}
 ```

## Mapping Your Data

The most crucial step is mapping your data to fit Tracardi's structure. Make sure all the necessary data properties
match the right parts of Tracardi. Once this is done, send it to Elasticsearch using your preferred programming
language.

## Importing CSV Data to Elasticsearch using Python

In this chapter we explain how to use Python to iterate through a CSV file containing fields such
as `first name`, `last name`, and `gender` and import this data into an Elasticsearch index. The Elasticsearch index
should follow the provided schema structure.

## Prerequisites

Before you begin, ensure you have the following:

- Elasticsearch server up and running.
- Python installed on your system.
- Elasticsearch Python client library (`elasticsearch-py`) installed.


## Necessary Information

To perform the data import to Tracardi, please ensure you have the following essential details:

1. **Elasticsearch Login and Password:**
   You will require the login credentials (username and password) for the Elasticsearch instance that is connected to
   Tracardi. If necessary, make modifications to the script provided below to include these login credentials.

2. **Last Event Index Name:**
   You will need to know the name of the most recent monthly event index created by Tracardi in Elasticsearch. Please
   check your Elasticsearch environment to determine the name of this index.

3. **Import Sequence:**
   The data import should follow a specific sequence to ensure proper data handling. Start by importing profiles, and
   subsequently, if required, import events and sessions. This order ensures that the essential profile data is in place
   before related events and sessions are imported.

## Steps

1. **Install the Elasticsearch Python Client**

   If you haven't already installed the Elasticsearch Python client, you can do so using pip:

   ```bash
   pip install elasticsearch
   ```

2. **Python Script for Data Import**

   Create a Python script that reads the CSV file, maps its data to the Elasticsearch schema, and sends the data to the
   Elasticsearch index. Here's a sample Python script to achieve this:

   ```python
   from elasticsearch import Elasticsearch
   import csv
   import uuid
   from datetime import datetime

   # Elasticsearch client setup
   es = Elasticsearch([{'host': 'your_elasticsearch_host', 'port': 9200}])

   # Open the CSV file
   with open('your_data.csv', mode='r') as csv_file:
       csv_reader = csv.DictReader(csv_file)

       # Iterate through each row in the CSV
       for row in csv_reader:
           # Create a unique identifier for each record
           unique_id = str(uuid.uuid4())

           # Prepare the data in the Elasticsearch schema
           data = {
               "id": unique_id,
               "ids": [unique_id],
               "metadata": {
                   "time": {
                       "insert": datetime.now().isoformat(),
                       "create": None,
                       "update": datetime.now().isoformat(),
                       "segmentation": None,
                       "visit": {
                           "last": None,
                           "current": datetime.now().isoformat(),
                           "count": 1,
                           "tz": "Your_Timezone"
                       }
                   },
                   "aux": {},
                   "status": None
               },
               "stats": {
                   "visits": 0,
                   "views": 0,
                   "counters": {}
               },
               "traits": {
                   "gender": row['gender']
               },
               "segments": [],
               "interests": {},
               "consents": {
                   "cookies": {
                       "revoke": None
                   }
               },
               "active": True,
               "aux": {
                   "geo": {
                       "continent": "Your_Continent"
                   }
               },
               "data": {
                   "pii": {
                       "firstname": row['first name'],
                       "lastname": row['last name'],
                       "name": row['first name'] + " " + row['last name']
                   },
                   # Add other data fields as needed
               }
           }

           # Send the data to Elasticsearch
           print(es.index(index='vendor.tracardi-event-2023-10', doc_type='_doc', body=data))

   print("Data import completed.")
   ```

   Replace placeholders like `'your_elasticsearch_host'`, `'your_data.csv'`, `'Your_Timezone'`, and other values with
   your specific details. Notice that the import is to the monthly index of the tracardi event `vendor.tracardi-event-2023-10`. Please check elasticsearch for the last monthly index that is created by tracardi. 

3. **Run the Python Script**

   Execute the Python script to import the data from the CSV file into your Elasticsearch index. You should see the "
   Data import completed" message upon successful execution.

Now, your CSV data is successfully imported into Elasticsearch with the specified schema.

### How to import event data through Tracardi endpoint?

You can use `/track` endpoint to import event data from CSV and map them with session and profile.

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
config = ('file1.csv', 'phone-call', 'session-id', 'profile-id')

source_id = "c437d599-5d38-43e2-84b9-c6267dce6410"

for row in read_csv(config[0]):

    mapped_properties = {
       "from": config[0]
       # Add the properties you need. Include them in the CSV to be able to 
       # map them here
    }
   
    payload = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": row[config[2]]  # If the session id does not exist system will create it for you
        },
        "profile": {
            "id": row[config[3]]
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