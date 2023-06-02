import os
from pprint import pprint

import weaviate


from docs_ai.utils import get_chat_gpt3_response

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
"How do I import mongodb data to tracardi."
"I got error Invalid API"
"How I I send email in Tracardi" # *
"Can I send marketing campaigns from tracardi"
"Can I send SMSes with tracardi" #
"How Do I install extensions" #


question = "Can Tracardi use ChatGPT"
nearText = {"concepts": [question]}

result = (
    client.query
    .get("Tracardi", ["question", "answer"])
    .with_additional(["distance"])
    .with_near_text(nearText)
    .with_limit(10)
    .do()
)

answers = []
for item in result['data']['Get']['Tracardi']:
    answers.append(item['answer'])

context = "\n-- new document part --\n".join(list(set(answers)))
prompt = f"""I have this documentation on Tracardi system. Use this information. Pick the most accurate document parts and
answer in detail the question: "{question}". If you think that the answer 
can not be found in provided information or the answer may be inaccurate respond with \"I can't answer this question\". 
Rephrase the information for more clarity. Respond only with answer.

Use this documentation: {context}
"""

print(f"RPMPT: {prompt}")
print("-----")
print(get_chat_gpt3_response(prompt[:4090]))
# print(json.dumps(result, indent=4))
