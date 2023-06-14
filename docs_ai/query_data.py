import json
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
"Does Tracardi have Mysql Plugin?"
"What is the syntax for the IF condition?"
"how to purge event, session, profile?"

question = """
How tracardi bot works?
"""

question = question.strip("?!.")

prompt = f"""
Rewrite question "{question}" to be more general. Respond only with question.
"""

general_question = get_chat_gpt3_response(prompt[:4090])

nearText = {"concepts": [question]}

result = (
    client.query
        .get("Tracardi", ["question", "answer", "file"])
        .with_additional(["distance", "certainty"])
        .with_near_text(nearText)
        .with_limit(5)
        .do()
)

answers = []
skip_answers = {}
for item in result['data']['Get']['Tracardi']:
    distance = item['_additional']['distance']
    certainty = item['_additional']['certainty']
    file = item['file']
    if distance > 0.2:
        continue
    if item['answer'] in skip_answers:
        continue
    skip_answers[item['answer']] = 1
    answers.append((item['answer'], distance, certainty, file))

pprint(answers)

documents = []
for answer, distance, certainty, file in answers:
    prompt = f"""Is the text I provided below related to the question: "{question.strip()}". Answer only YES or NO 
    Text: {answer}"""

    yes_no = get_chat_gpt3_5_response(
        system=f"Your objective is to find the best document related the question: '{question.strip()}' "
               f"and return YES or NO",
        user=prompt[:4090],
        assistant=""
        # assistant=f"""Previous answer context:
        # {chatgpt3_context}
        # """
    )
    if yes_no['content'] == 'YES':
        documents.append((answer, distance, certainty, file))

if not documents:
    print("No data in documentation")
    exit()

context = ""
n = 0
for answer, distance, certainty, file in documents:
    n += 1
    context += f"\n\n-- Document {file} (Distance: {distance}, Certainty: {certainty}) --\n{answer}"

prompt = f"""I have this documentation on Tracardi system. Answer question "{general_question} {question}". 
Respond with one detailed answer. Respond only if you are sure of the answer correctness, otherwise say "I don't know answer
to this question".

Use this documentation: {context}
"""

print(f"RPMPT: {prompt}")

# print("--CHAT3---")
# chatgpt3_context = get_chat_gpt3_response(prompt[:4090])
# print(chatgpt3_context)
print("---CHAT4---")
response = get_chat_gpt3_5_response(
    system="You are an expert on Tracardi system with the access to MD files with documentation. "
           "Your name is Tracardi Bot. "
           "You will be given a set of documents and their distance to question. "
           "The smaller distance the better source of information. Use the documents, "
           "to answer the question as good as possible using all the available information. "
           "Remember that examples are good way of answering the questions. "
           "So if an example is available in documents "
           "and is needed to explain and answer the question include the example as well. "
           "Give as verbose information as possible.",
    user=prompt[:4090],
    assistant=""
    # assistant=f"""Previous answer context:
    # {chatgpt3_context}
    # """
)

print(response['content'])
# print(json.dumps(result, indent=4))
