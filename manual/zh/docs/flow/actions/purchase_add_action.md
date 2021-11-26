# Profile Purchase Add Action

# Input

Plugin takes payload as input. From this payload plugin takes the following data:
```
{
    "name": product_name,
    "price": product_price,
    "quantity": quantity,
    "source": {
        "id": source_id
    }
    "profile": {
        "id": profile_id
    }
}
```
This data is validated due to these types:
```
product_name: str
price: float
quantity: int
source_id: str
profile_id: str
```
Then this data is used to create a new document in a proper index of ElasticSearch database, describing one purchase.

# Output

Plugin returns an instance of Result class, with `"payload"` as parameter `port` and a dictionary 
with one key in form of `"msg"` and one value in form of `True` if the document was created with 
no errors and other issues, or string containing error's name, if an error occurred during creating the document. 