# Full contact webhook

FullContact.com is an Identity Resolution Platform. It allows you to resolve and enrich people by submitting any
identifiers you already have, such as a personal email address, work email address, phone number, name and home address,
social ID, social URL and social username (except Facebook and Instagram).

In order to use FullContact you wil have to obtain an API_KEY that will allow you to access FullContact API.  
To do that go to fullcontact.com, register and follow the steps on the page.

# Configuration

Example of configuration.

```json
{
  "source": {
    "id": "resource-id"
  },
  "pii": {
    "email": "email@email.com",
    "emails": [
      "email1@email.com",
      "email2@email.com"
    ],
    "phone": "+1838747734",
    "phones": [
      "+1838747734",
      "+1838747735"
    ],
    "location": null,
    "name": "Adam"
  }
}
```

*Configuration schema description*

* `resource-id` must be valid id from resource list that points to FullContact api key. Please see below the schema of
  the credentials.
* `pii` does not need all the data from example. It is ok to provide only `e-mail` or `phone`.

*Example of FullContact resource credentials*

Use `api-token` type of resource to configure fullcontact credentials.

```json
{
  "token": "<API_KEY>"
}
```

`<API_KEY>` must be replaced by API_KEY provided by FullContact service.

*Example of `pii` data*

This configuration is valid too:

```json
{
  "source": {
    "id": "<resource-id>"
  },
  "pii": {
    "email": "email@email.com"
  }
}
```

The more data you provide th better as FullContact will be able to match the person more precisely.

You can use dotted notation to access data from profile or event. This can be done like this.

```json
{
  "source": {
    "id": "<resource-id>"
  },
  "pii": {
    "email": "profile@traits.private.email"
  }
}
```

String `profile@traits.private.email` will be replaced with the value (path to value `traits.private.email`) from
profile.

# Input

This action does not need payload.

# Output

If the connection to FullContact was successful the port payload will return the response data. 
Otherwise, the payload port will be inactive and the error message will be returned on error port. 

*Example of successful response on port payload*

```json
{
  "status": 200,
  "body": {
    "fullName": "Kazi Amki",
    "ageRange": null,
    "gender": "Male",
    "location": "Sao Paulo",
    "title": "Film Writer",
    "organization": "Freelance",
    "linkedin": null,
    "facebook": null,
    "bio": null,
    "website": null,
    "details": {
      "name": {
        "given": "Kazi",
        "family": "Amki",
        "full": "Kazi Amki"
      },
      "age": null,
      "gender": "Male",
      "demographics": {
        "gender": "Male"
      },
      "emails": [],
      "phones": [],
      "locations": [
        {
          "region": "Sao Paulo",
          "country": "Brazil",
          "countryCode": "BR",
          "formatted": "Sao Paulo"
        }
      ],
      "employment": [
        {
          "name": "Freelance",
          "current": true,
          "title": "Film Writer"
        }
      ],
      "photos": [],
      "education": [
        {
          "name": "ECA - USP",
          "degree": "Publishing"
        }
      ],
      "urls": [],
      "interests": []
    },
    "updated": "2021-06-16"
  }
}
```