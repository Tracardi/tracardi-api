import os

import weaviate
import json

client = weaviate.Client(
    url="http://192.168.1.190:8080/",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get('API_KEY', "None")  # Replace with your inference API key
    }
)

nearText = {"concepts": ["how tracardi tracks profiles"]}

result = (
    client.query
    .get("Question", ["question", "answer"])
    .with_additional(["distance"])
    .with_near_text(nearText)
    .with_limit(10)
    .do()
)

print(json.dumps(result, indent=4))
