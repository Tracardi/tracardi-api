# How to make the initial loading of the data and how to update it constantly? We want to add user data to the profile from an external resource (Database). And how to upload a new profile if we have nothing on the user in Tracardi?

The simplest method is to execute a script that retrieves data from your database and uses the `/track` endpoint to insert the data. Importing is quite similar to collecting data. You will need to convert your database records into the Tracardi profile format.

Here are the steps:

1. Create an event source in Tracardi for the import.
2. Note down the event source ID, as you will need it later.
3. Develop a basic script that connects to your database and fetches the profiles you wish to import.
4. Process each data record and adapt it to the following schema. If your profile IDs are numbers, convert them to an MD5 hash with some added 'salt' for security reasons, as using plain numbers can be risky. Not all fields must ne filled. Remove unnecessary ones:
```json
{
 "pii": {
  "firstname": "string",
  "lastname": "string",
  "name": "string",
  "birthday": "2010-01-01 00:00:00",
  "language": {
   "native": "string",
   "spoken": [
    "string"
   ]
  },
  "gender": "string",
  "education": {
   "level": "string"
  },
  "civil": {
   "status": "string"
  },
  "attributes": {
   "height": 0,
   "weight": 0,
   "shoe_number": 0
  }
 },
 "identifier": {
  "id": "string",
  "token": "string",
  "passport": "string",
  "credit_card": "string",
  "coupons": [
   "string"
  ],
  "badge": "string"
 },
 "contact": {
  "email": "string",
  "phone": "string",
  "app": {
   "whatsapp": "string",
   "discord": "string",
   "slack": "string",
   "twitter": "string",
   "telegram": "string",
   "wechat": "string",
   "viber": "string",
   "signal": "string"
  },
  "address": {
   "town": "string",
   "county": "string",
   "country": "string",
   "postcode": "string",
   "street": "string",
   "other": "string"
  }
 },
 "media": {
  "image": "string",
  "webpage": "string",
  "social": {
   "twitter": "string",
   "facebook": "string",
   "youtube": "string",
   "instagram": "string",
   "tiktok": "string",
   "linkedin": "string",
   "reddit": "string"
  }
 },
 "job": {
  "position": "string",
  "salary": 10,
  "type": "string",
  "company": {
   "name": "string",
   "size": 100,
   "segment": "string",
   "country": "string"
  },
  "department": "string"
 },
 "preferences": {
  "purchases": [
   "string"
  ],
  "colors": [
   "string"
  ],
  "sizes": [
   "string"
  ],
  "devices": [
   "string"
  ],
  "channels": [
   "string"
  ],
  "payments": [
   "string"
  ],
  "brands": [
   "string"
  ],
  "fragrances": [
   "string"
  ],
  "services": [
   "string"
  ],
  "other": [
   "string"
  ]
 },
 "loyalty": {
  "codes": [
   "string"
  ],
  "card": {
   "id": "string",
   "name": "string",
   "issuer": "string",
   "expires": "2022-01-01 00:00:00",
   "points": 0
  }
 }
}
```
5. Use the `/track` endpoint on your Tracardi API to send the following data payload:
```json
{
    "source": {
        "id": "<source_id>"
    },
    "profile": {
        "id": "<profile-id-from-your-system>"
    },
    "events": [
        {
            "type": 'profile-update',
            "properties": <mapped-profile>
        }
    ]
}

```

The 'profile-update' event will transfer the provided properties to your Tracardi profile. The same way you can update the profile data. 

