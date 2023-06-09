import hashlib
import json
import os
import shutil

from docs_ai.utils import get_markdown, get_chat_gpt3_response

_local_dir = os.path.dirname(__file__)


def summary_file_name(file_name):
    return os.path.join(_local_dir, "content/summary", file_name)


def has_summary(file_name) -> bool:
    file_name = summary_file_name(file_name)
    return os.path.exists(file_name) and os.path.isfile(file_name)


def save_summary(file_name, content):
    file_name = summary_file_name(file_name)
    save_content(file_name, content)


def create_folder_if_not_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)


def save_content(file_name, content):
    # Save the content to a file with the hash as the file name
    with open(file_name, 'w') as file:
        file.write(content)


def process(file_path, content) -> bool:
    if content == "" or len(content) < 100:
        return False

    summary_file_name = file_path.replace("/", "."). \
        replace('.home.risto.PycharmProjects.tracardi-api.', '')

    if has_summary(summary_file_name):
        return False

    prompt = f"""Write a verbose summary of information included in the documentation text. 
            Do no use any code just plain text explanation 
            what information is included in the text. Include all most important information
            that you can later use to look up this content. Return at least two paragraphs if text
            is longer then 1000 letters. 
            
            Documentation: {content}
            """
    if len(content) > 4096:
        print("Too long", file_path)
        return False

    summary = get_chat_gpt3_response(prompt)
    save_summary(summary_file_name, summary)

    return True


def yield_paragraphs(document):
    chunk = ""
    for line in document.split("\n"):
        if line.startswith("# "):
            if chunk:
                yield chunk.strip()
            chunk = line
        else:
            chunk += f"{line}\n"
    if chunk:
        yield chunk.strip(" -")


def move_file(source_folder, destination_folder, filename):
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)

    try:
        shutil.move(source_path, destination_path)
        print(f"File '{filename}' moved successfully!")
    except FileNotFoundError:
        print(f"File '{filename}' not found in '{source_folder}'!")
    except shutil.Error as e:
        print(f"Error occurred while moving file '{filename}': {str(e)}")


def chunk_string(string, chunk_size):
    if len(string) <= chunk_size:
        return [string]
    chunks = []
    for i in range(0, len(string), chunk_size):
        chunks.append(string[i:i + chunk_size])
    return chunks


# Example usage

directory = os.path.join(_local_dir, '../docs')

docs_directory = os.path.join(_local_dir, 'content/documentation')
create_folder_if_not_exists(docs_directory)

question_directory = os.path.join(_local_dir, 'content/question')
create_folder_if_not_exists(question_directory)
os.chdir(question_directory)

number_of_paragraphs = 0
for i, (file_name, document) in enumerate(get_markdown(directory)):

    if document == "":
        continue

    short_file_name = file_name.replace('/home/risto/PycharmProjects/tracardi-api/', '')
    # Skip plugin documentation
    if short_file_name.startswith('docs/flow/action'):
        continue

    print(f"Processing: {file_name}")
    # result = process(file_name, document)
    # print(i, file_name, result)

    _short_file_name = None
    if short_file_name.startswith('docs/'):
        _short_file_name = short_file_name[5:]
        _short_file_name = _short_file_name.replace("/", "_")
        _short_file_name = _short_file_name.split('.')[0]
        create_folder_if_not_exists(f"{docs_directory}/{_short_file_name}")

    for main_paragraph in yield_paragraphs(document):

        paragraphs = chunk_string(main_paragraph, 4000)

        for paragraph in paragraphs:

            if len(paragraph) < 50:
                print(f"Skipped document {file_name}, paragraph `{paragraph}`.")
                continue

            number_of_paragraphs += 1
            sha1_hash = hashlib.sha1(paragraph.encode()).hexdigest()
            file = f"{sha1_hash}.json"

            data_file = os.path.join(docs_directory, _short_file_name, file)

            if os.path.exists(file) and os.path.isfile(file):
                shutil.move(file, data_file)
                print(f"Moved {file}")
                continue

            if os.path.exists(data_file) and os.path.isfile(data_file):
                print(f"   Skipped {data_file}")
                continue

            prompt = f"What question the following text answers. Give one question that covers the whole content. " \
                     f"And at least 2 or 3 optional questions that cover only part of the text. Try to write qeiestion in " \
                     f"form of \"How to?\" or \"What is\" if possible." \
                     f"Text is in markdown format. Write only one question per line, nothing else." \
                     f"Text:\n{paragraph}\n\n"

            json_question = get_chat_gpt3_response(prompt)
            print(json_question)
            questions = json_question.split("\n")
            questions = [q for q in questions if q != "Optional questions:" and q != ""]
            json_content = {
                "file_name": file_name.replace('/home/risto/PycharmProjects/tracardi-api/', ''),
                "questions": questions,
                "answer": paragraph
            }

            save_content(data_file, json.dumps(json_content))
