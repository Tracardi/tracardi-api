import os
from pprint import pprint

import weaviate

from docs_ai.utils import get_chat_gpt3_response, get_chat_gpt3_5_response

client = weaviate.Client(
    url="http://192.168.1.190:8080/",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get('API_KEY', "None")  # Replace with your inference API key
    }
)

def record_exists(hash):
    where_filter = {
        "path": ["hash"],
        "operator": "Equal",
        "valueText": hash,
    }

    return (
        client.query
            .get("Tracardi", ["question", "answer", 'file', 'hash'])
            .with_where(where_filter)
            .do()
    )

