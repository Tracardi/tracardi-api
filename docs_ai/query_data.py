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

"What are the key definitions in tracardi"
"What is session"
"How can I bind event to button click"
"What is profile"
"Where tracardi stores profile visits."
"What is dot notation."
"How do I filter the data."
"How do I import mongodb data to tracardi."
"I got error Invalid API"
"How I I send email in Tracardi"  # *
"Can I send marketing campaigns from tracardi"
"Can I send SMSes with tracardi"  #
"How Do I install extensions"  #

question = """
How can I use reports in Tracardi?
"""

prompt = f"""
Rewrite question "{question}" to be more general. Respond only with question.
"""

general_question = get_chat_gpt3_response(prompt[:4090])

nearText = {"concepts": [question]}

result = (
    client.query
        .get("Tracardi", ["question", "answer"])
        .with_additional(["distance", "certainty"])
        .with_near_text(nearText)
        .with_limit(10)
        .do()
)

answers = []
skip_answers = {}
for item in result['data']['Get']['Tracardi']:
    distance = item['_additional']['distance']
    if distance > 0.2:
        continue
    if item['answer'] in skip_answers:
        continue
    skip_answers[item['answer']] = 1
    answers.append((item['answer'], distance))

context = ""
n = 0
for answer, distance in answers:
    n += 1
    context += f"\n\n-- Document part {n} (Distance: {distance}) --\n{answer}"

prompt = f"""I have this documentation on Tracardi system. Answer two questions. The general question 
"{general_question}" and the user specific question: "{question}". Respond with one combined answer.
Respond only if you are sure of the answer correctness, otherwise say "I don't know answer to this question".

Use this documentation: {context}
"""

print(f"RPMPT: {prompt}")

print("--CHAT3---")
chatgpt3_context = get_chat_gpt3_response(prompt[:4090])
print(chatgpt3_context)
print("---CHAT4---")
response = get_chat_gpt3_5_response(
    system="You are an expert on Tracardi system with the access to MD files with documentation. "
           "You will be given a set of documents and their distance to question. "
           "The smaller distance the better source of information. Use the most accurate documents, "
           "combine them, to answer the question in detail. If a code example available in documents "
           "and is needed to explain "
           "and answer the question include the code as well.",
    user=prompt[:4090],
    assistant=""
    # assistant=f"""Previous answer context:
    # {chatgpt3_context}
    # """
)

print(response['content'])
# print(json.dumps(result, indent=4))
