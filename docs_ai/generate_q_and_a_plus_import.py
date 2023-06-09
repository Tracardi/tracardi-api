import hashlib
import json
import os

import weaviate

from docs_ai.utils import get_markdown, get_chat_gpt3_response

_local_dir = os.path.dirname(__file__)


def record_exists(client, hash):
    where_filter = {
        "path": ["hash"],
        "operator": "Equal",
        "valueText": hash,
    }

    return (
        client.query
            .get("Tracardi", ["question", "answer", 'file', 'hash'])
            .with_where(where_filter)
            .do()
    )


def delete_records(client, file_name):
    where_filter = {
        "path": ["file"],
        "operator": "Equal",
        "valueText": file_name,
    }

    response = (
        client.query
            .get("Tracardi", ["question", "answer", 'file', 'hash'])
            .with_additional(["id"])
            .with_where(where_filter)
            .do()
    )
    for item in response['data']['Get']['Tracardi']:
        client.data_object.delete(uuid=item['_additional']['id'], class_name="Tracardi")



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


def delete_files_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        print("All files deleted successfully!")
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    except Exception as e:
        print(f"An error occurred while deleting files: {str(e)}")


def chunk_string(string, chunk_size):
    if len(string) <= chunk_size:
        return [string]
    chunks = []
    for i in range(0, len(string), chunk_size):
        chunks.append(string[i:i + chunk_size])
    return chunks


def get_content_and_paragraph_hash(document):
    for content in yield_paragraphs(document):
        for paragraph in chunk_string(content, 4000):

            if len(paragraph) < 50:
                print(f"Skipped document {file_name}, paragraph to short: `{paragraph}`.")
                continue

            yield paragraph, hashlib.sha1(paragraph.encode()).hexdigest()


def get_short_file_name(file_name):
    _short_file_name = file_name.replace('/home/risto/PycharmProjects/tracardi-api/', '')
    _short_file_name = _short_file_name[5:]
    _short_file_name = _short_file_name.replace("/", "_")
    _short_file_name = _short_file_name.split('.')[0]
    return _short_file_name


def has_content(file_name, content_hash):
    file = f"{content_hash}.json"
    short_file_name = get_short_file_name(file_name)
    content_file = os.path.join(docs_directory, short_file_name, file)
    if not os.path.exists(content_file) or not os.path.isfile(content_file):
        return False
    return True


def has_correct_data(file_name, content) -> bool:
    for _, paragraph_hash in get_content_and_paragraph_hash(content):
        if not has_content(file_name, paragraph_hash):
            return False
    return True


# Connect to Weaviate
key = os.environ.get('API_KEY', "None")

client = weaviate.Client(
    url="http://192.168.1.190:8080",  # Replace with your endpoint
    additional_headers={
        "X-OpenAI-Api-Key": key  # Replace with your inference API key
    }
)

try:
    class_obj = {
        "class": "Tracardi",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "vectorizeClassName": True
            }
        }
    }
    # client.schema.delete_class("Tracardi")
    client.schema.create_class(class_obj)
except weaviate.exceptions.UnexpectedStatusCodeException:
    pass

# Example usage

directory = os.path.join(_local_dir, '../docs')

docs_directory = os.path.join(_local_dir, 'content/documentation')
hash_directory = os.path.join(_local_dir, 'content/hashes')
create_folder_if_not_exists(docs_directory)

question_directory = os.path.join(_local_dir, 'content/question')
create_folder_if_not_exists(question_directory)
os.chdir(question_directory)

number_of_paragraphs = 0
with client.batch as batch:
    batch.batch_size = 10
    for i, (file_name, content) in enumerate(get_markdown(directory)):

        if content == "":
            continue

        short_file_name = file_name.replace('/home/risto/PycharmProjects/tracardi-api/', '')
        # Skip plugin documentation
        if short_file_name.startswith('docs/flow/action'):
            continue

        # Generate document hash

        doc_hash = hashlib.sha1(content.encode()).hexdigest()

        docs_hash_file = os.path.join(hash_directory, doc_hash)
        if os.path.exists(docs_hash_file) and os.path.isfile(docs_hash_file):
            # File did not change
            print(f"File {file_name} did  not change.")

            if has_correct_data(file_name, content):
                print(f"   Skipped {file_name}")
                continue

        # Script will not cross this point if the content is ok and has not changed.

        _short_file_name = get_short_file_name(file_name)
        file_folder = f"{docs_directory}/{_short_file_name}"

        print("go", file_name, "short", file_folder)

        create_folder_if_not_exists(file_folder)
        delete_files_in_folder(file_folder)

        # Delete record for all hashes under the file_folder

        delete_records(client, file_name.replace('/home/risto/PycharmProjects/tracardi-api/', ''))

        # If we are able to create a content folder and delete all old content we can mark it as OK.

        save_content(docs_hash_file, "1")

        print(f"Processing: {file_name}")
        # result = process(file_name, document)
        # print(i, file_name, result)
        for paragraph, paragraph_hash in get_content_and_paragraph_hash(content):
            number_of_paragraphs += 1
            file = f"{paragraph_hash}.json"

            data_file = os.path.join(docs_directory, _short_file_name, file)

            # If hash file does not exist it means the content has changed.

            prompt = f"What question the following text answers. Give one question that covers the whole content. " \
                     f"And at least 2 or 3 optional questions that cover only part of the text. Try to write question in " \
                     f"form of \"How to?\" or \"What is\" if possible." \
                     f"Text is in markdown format. Write only one question per line, nothing else." \
                     f"Text:\n{paragraph}\n\n"

            json_question = get_chat_gpt3_response(prompt)
            questions = json_question.split("\n")
            questions = [q for q in questions if q != "Optional questions:" and q != ""]
            json_content = {
                "file_name": file_name.replace('/home/risto/PycharmProjects/tracardi-api/', ''),
                "questions": questions,
                "answer": paragraph,
                "hash": paragraph_hash
            }

            save_content(data_file, json.dumps(json_content))

            response = record_exists(client, paragraph_hash)

            if len(response['data']['Get']['Tracardi']) == 0:
                print("Saving to vector store.")
                client.batch.add_data_object(json_content, "Tracardi")
