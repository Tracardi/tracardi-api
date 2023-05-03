import json
import os


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
