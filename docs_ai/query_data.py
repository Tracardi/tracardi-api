import os
from pprint import pprint

import weaviate


from docs_ai.utils import get_ai_response

client = weaviate.Client(
    url="http://192.168.1.190:8080/",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get('API_KEY', "None")  # Replace with your inference API key
    }
)

"What are the key definitions in tracardi"
"What is session"
"How can I bind event to button click"
"What is profile"
"Where tracardi stores profile visits."
"What is dot notation."
"How do I filter the data."

question = "How do I import data to tracardi."
nearText = {"concepts": [question]}

result = (
    client.query
    .get("Question", ["question", "answer"])
    .with_additional(["distance"])
    .with_near_text(nearText)
    .with_limit(30)
    .do()
)

answers = []
for item in result['data']['Get']['Question']:
    answers.append(item['answer'])

context = "\n".join(list(set(answers)))
prompt = f"""You are an expert on Tracardi system. Answer the question: {question}
Here is the information you should use. It may be inaccurate in some parts. Please extract the most accurate and 
answer in detail so a 16 year old could understand. Use only provided information. If you do not think that the answer 
can not be found in provided information or the answer may be inaccurate respond with \"I can't answer this question\". 
Information from tracardi documentation: {context}
"""

print(get_ai_response(prompt[:4090]))
# print(json.dumps(result, indent=4))
