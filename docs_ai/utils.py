import json
import os

import openai

openai.api_key = os.environ.get('API_KEY', None)


def get_markdown(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    # Parse the markdown file and extract paragraphs
                    markdown_text = file.read()
                    yield os.path.realpath(file_path), markdown_text.strip()


def get_jsons(folder_path):
    # iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # check if the file is a JSON file
        if filename.endswith(".json"):
            # read the JSON file
            with open(os.path.join(folder_path, filename)) as json_file:
                data = json.load(json_file)
                # do something with the JSON data
                yield data


def get_ai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text.strip()
