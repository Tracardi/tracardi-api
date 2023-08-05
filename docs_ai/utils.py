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


def extract_filename(full_path):
    filename_with_extension = os.path.basename(full_path)
    filename, _ = os.path.splitext(filename_with_extension)
    return filename

def get_jsons(folder_path):
    # iterate over all subfolders and files in the folder
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # check if the file is a JSON file
            if filename.endswith(".json"):
                # read the JSON file
                with open(os.path.join(root, filename)) as json_file:
                    data = json.load(json_file)
                    # do something with the JSON data
                    yield data, extract_filename(json_file.name)


def get_chat_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text.strip()


def get_chat_gpt3_5_response(system, assistant, user):
    query = {
        'model': 'gpt-3.5-turbo',
        'messages': [{"role": "system", "content": system},
                     {"role": "user", "content": user},
                     {"role": "assistant", "content": assistant}]
    }
    response = openai.ChatCompletion.create(**query)

    return response.choices[0].message.content
