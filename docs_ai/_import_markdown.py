import os

import weaviate

from docs_ai.utils import get_markdown

_local_dir = os.path.dirname(__file__)
directory = os.path.join(_local_dir, '../docs')


def chunk_string(s, chunk_size=4000):
    """Split a string into chunks of the given size."""
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


client = weaviate.Client(
    url="http://192.168.1.190:8080",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get('API_KEY', "None")  # Replace with your inference API key
    }
)

try:
    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
    }

    client.schema.create_class(class_obj)
except weaviate.exceptions.UnexpectedStatusCodeException:
    pass

i = 0
# Configure a batch process
with client.batch as batch:
    batch.batch_size = 100

    for i, (file_name, document) in enumerate(get_markdown(directory)):

        if document == "":
            continue

        for chunk in chunk_string(document):
            i += 1
            print(f"importing question: {i + 1}")
            properties = {
                "answer": chunk,
                "question": "question",
                "file": file_name,
            }
            # print(properties)
            client.batch.add_data_object(properties, "Question")
