import weaviate
import os

from docs_ai.utils import get_jsons

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
    # Batch import all Questions
    for d in get_jsons('content/question'):
        for question in d['questions']:
            i += 1
            print(f"importing question: {i + 1}")
            properties = {
                "answer": d["answer"],
                "question": question,
                "file": d["file_name"],
            }

            client.batch.add_data_object(properties, "Question")
