import weaviate
import os

from docs_ai.utils import get_jsons


def record_exists(client, hash):
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


key = os.environ.get('API_KEY', "None")

client = weaviate.Client(
    url="http://192.168.1.190:8080",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": key  # Replace with your inference API key
    }
)

try:
    class_obj = {
        "class": "Tracardi",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "vectorizeClassName": True
            }
        }
    }
    # client.schema.delete_class("Tracardi")
    client.schema.create_class(class_obj)
except weaviate.exceptions.UnexpectedStatusCodeException:
    pass

i = 0
# Configure a batch process
with client.batch as batch:
    batch.batch_size = 10
    # Batch import all Questions
    for d, hash in get_jsons('content/documentation'):
        questions = "\n".join(d['questions'])
        i += 1
        print(f"importing question: {i + 1}")
        properties = {
            "answer": d["answer"],
            "question": questions,
            "file": d["file_name"],
            "hash": hash
        }
        print(properties)
        response = record_exists(client, hash)
        print(len(response['data']['Get']['Tracardi']))
        # client.batch.add_data_object(properties, "Tracardi")
