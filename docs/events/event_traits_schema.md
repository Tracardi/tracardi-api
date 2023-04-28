# Event traits schema

This is a simplified event traits schema. This type of schema will be created when you stick to predefined events. 

```json
{
  "name": "string",
  "type": "string",
  "traits": {
    "identifier": {
      "id": "string",
      "token": "string",
      "passport": "string",
      "login": "string",
      "credit_card": "string",
      "coupon": "string",
      "badge": "string"
    },
    "contact": {
      "address": {
        "town": "string",
        "county": "string",
        "country": "string",
        "postcode": "string",
        "street": "string"
      },
      "phone": "string",
      "app": {
        "email": "string",
        "twitter": "string",
        "whatsapp": "string",
        "discord": "string",
        "slack": "string",
        "telegram": "string",
        "wechat": "string",
        "viber": "string",
        "signal": "string"
      }
    },
    "pii": {
       "firstname": "string",
       "lastname": "string"
    },
    "marketing": {
      "coupon": "string",
      "channel": "string",
      "promotion": {
        "id": "string",
        "name": "string"
      }
    },
    "loyalty": {
      "card": {
        "id": "string",
        "name": "string",
        "issuer": "string",
        "expires": "datetime"
      }
    },
    "payment": {
      "method": "string",
      "credit_card": {
        "number": "string",
        "expires": "string",
        "holder": "string"
      }
    },
    "ec": {
      "order": {
        "id": "string",
        "status": "string",
        "income": {
          "value": "float",
          "revenue": "float"
        },
        "cost": {
          "shipping": "float",
          "tax": "float",
          "discount": "float",
          "other": "float"
        },
        "affiliation": "string"
      },
      "checkout": {
        "id": "string",
        "currency": "string",
        "value": "string"
      },
      "product": {
        "id": "string",
        "name": "string",
        "sku": "string",
        "category": "string",
        "brand": "string",
        "variant": {
          "name": "string",
          "color": "string",
          "size": "string"
        },
        "price": "float",
        "quantity": "int",
        "position": "int",
        "review": "string",
        "rate": "integer"
      }
    },
    "query": {
      "type": "string",
      "string": "string"
    }
  }
}

```