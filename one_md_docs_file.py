import os


def find_md_files(root_folder, skip_folders=None):
    md_files = []
    if skip_folders is None:
        skip_folders = []

    for root, dirs, files in os.walk(root_folder):
        for folder_to_skip in skip_folders:
            if folder_to_skip in dirs:
                dirs.remove(folder_to_skip)  # Skip the specified folder
        for file in files:
            if file.endswith('.md'):
                _file = os.path.join(root, file)
                print(_file)
                md_files.append(_file)
    return md_files


def merge_md_files(md_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as merged_file:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as source_file:
                merged_file.write(source_file.read())
                merged_file.write('\n\n')  # Add a blank line between merged files


if __name__ == "__main__":
    root_folder = "/home/risto/PycharmProjects/tracardi-api/docs"  # Replace with the path to your folder
    output_file = "documentation.md"  # Name of the merged output file
    skip_folders = ['ai', 'hacktoberfest']  # Specify folders to skip (e.g., 'ai')

    md_files = find_md_files(root_folder, skip_folders)

    if md_files:
        merge_md_files(md_files, output_file)
        print(f"Merged {len(md_files)} .md files into {output_file}")
    else:
        print("No .md files found in the specified folder.")
