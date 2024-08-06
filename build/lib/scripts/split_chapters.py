#!/usr/bin/env python3
import os
import re
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

def split_into_chapters(text):
    # Split the text by chapter markers
    chapter_splits = re.split(r'(@@ .*? @@)', text, flags=re.DOTALL)
    chapters = []

    # Ensure the split text includes titles and contents
    if chapter_splits[0].strip() == '':
        chapter_splits = chapter_splits[1:]

    for i in range(0, len(chapter_splits), 2):
        chapter_title = chapter_splits[i].strip()
        chapter_content = chapter_splits[i + 1].strip() if (i + 1) < len(chapter_splits) else ''
        chapters.append((chapter_title, chapter_content))

    return chapters

def process_text_file(input_file_path, output_directory, info_output_directory):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract and save book info before the first @@ marker
    if '@@' in text:
        book_info = text.split('@@', 1)[0].strip()
        info_file_path = os.path.join(info_output_directory, os.path.basename(input_file_path).replace('.txt', '_info.txt'))
        with open(info_file_path, 'w', encoding='utf-8') as info_file:
            info_file.write(book_info)
        print(f"Book info saved to: {info_file_path}")

        # Start processing from the first @@ marker
        text = text.split('@@', 1)[1]
        text = '@@' + text  # Add the marker back to the beginning

    chapters = split_into_chapters(text)

    for index, (title, content) in enumerate(chapters):
        chapter_number = re.findall(r'\d+', title)[0] if re.findall(r'\d+', title) else str(index + 1)
        output_file_name = f"Chapitre_{chapter_number}.txt"
        output_file_path = os.path.join(output_directory, output_file_name)
        
        # Format the content with the chapter title starting at the beginning of the file
        formatted_content = f"{title}\n\n{content}"

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_content.strip())
        print(f"Processed file saved to: {output_file_path}")

def process_directory(input_directory, output_directory, info_output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    if not os.path.exists(info_output_directory):
        os.makedirs(info_output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_directory, file_name)
            print(f"Processing {file_name}...")
            process_text_file(input_file_path, output_directory, info_output_directory)
            print(f"Processed file: {file_name}")

if __name__ == "__main__":
    input_directory = os.path.join(base_dir, 'txt_processed/1-page_nb_cln')
    output_directory = os.path.join(base_dir, 'txt_processed/2-chapter_split')
    info_output_directory = os.path.join(base_dir, 'txt_processed/10-book_info')

    process_directory(input_directory, output_directory, info_output_directory)
    print("Script completed")
