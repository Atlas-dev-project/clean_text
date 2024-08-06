#!/usr/bin/env python3
import os
import re
import unicodedata
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

# Function to highlight chapter titles
def highlight_titles(text, titles):
    log_entries = []
    marked_titles = set()

    # Normalize text to ensure consistency in accent handling
    normalized_text = unicodedata.normalize('NFC', text)

    for title in titles:
        # Normalize the title
        normalized_title = unicodedata.normalize('NFC', title)

        # Split the title into chapter and title parts
        parts = normalized_title.split(' ', 2)
        chapter = ' '.join(parts[:2])
        chapter_title = parts[2] if len(parts) > 2 else ''

        # Ensure the pattern matches the chapter title format with possible line breaks, varying whitespace, and optional punctuation
        title_pattern = re.compile(r'(^' + re.escape(chapter) + r'[\s\S]*?' + re.escape(chapter_title) + r')', re.MULTILINE)
        alt_title_pattern = re.compile(r'(^' + re.escape(chapter) + r'[\s\S]+?' + re.escape(chapter_title) + r')', re.MULTILINE)

        # Only mark the title if it hasn't been marked yet
        if normalized_title not in marked_titles:
            new_title = r'@@ \1 @@'
            normalized_text, count = title_pattern.subn(new_title, normalized_text, count=1)  # Mark only once
            if count == 0:
                normalized_text, count = alt_title_pattern.subn(new_title, normalized_text, count=1)  # Mark only once
            if count > 0:
                log_entries.append(f"Added markers to title: {normalized_title}, Occurrences: {count}")
                marked_titles.add(normalized_title)
            else:
                log_entries.append(f"Title not found in text: {normalized_title}")

    return normalized_text, log_entries

# Function to remove standalone numbers, skipping lines with '@@'
def remove_numbers(text):
    log_entries = []

    def replace_number(match):
        line = match.group(0)
        if '@@' in line:
            return line  # Skip lines with '@@'
        else:
            number = int(match.group(2))
            log_entries.append(f"Removed number: {number}")
            return match.group(1) + match.group(3)

    number_pattern = re.compile(r'(\s+)(\d+)(\s*\n\s*\n)')
    cleaned_text = number_pattern.sub(replace_number, text)

    return cleaned_text, log_entries

# Function to remove phrases at the start of paragraphs
def remove_phrase_at_paragraph_start(text, phrases):
    log_entries = []

    for phrase in phrases:
        phrase_pattern = re.compile(r'(?<=\n\n)' + re.escape(phrase) + r'(?=\s)', re.MULTILINE)
        text, count = phrase_pattern.subn('', text)
        if count > 0:
            log_entries.append(f"Removed phrase: {phrase}")

    return text, log_entries

def process_text_file(input_file_path, output_file_path, log_file_path, phrases, titles):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract book info before the first @@ marker
    if '@@' in text:
        book_info = text.split('@@', 1)[0].strip()
        text = text.split('@@', 1)[1]
        text = '@@' + text  # Add the marker back to the beginning

    # Highlight titles
    highlighted_text, title_log_entries = highlight_titles(text, titles)

    # Remove phrases at the start of paragraphs (after the first @@ marker)
    book_info, remaining_text = highlighted_text.split('@@', 1)
    cleaned_text, phrase_log_entries = remove_phrase_at_paragraph_start('@@' + remaining_text, phrases)

    # Remove standalone numbers
    cleaned_text, number_log_entries = remove_numbers(cleaned_text)

    # Combine book info with cleaned text
    final_text = book_info.strip() + '\n\n' + cleaned_text

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(final_text.strip())

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("\n".join(title_log_entries + number_log_entries + phrase_log_entries))

def process_directory(input_directory, output_directory, log_directory, phrases, titles):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)
            log_file_path = os.path.join(log_directory, f'log_{os.path.splitext(file_name)[0]}.txt')

            print(f"Processing {file_name}...")
            process_text_file(input_file_path, output_file_path, log_file_path, phrases, titles)
            print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    input_directory = os.path.join(base_dir, "txt_processed/0-main_txt")
    output_directory = os.path.join(base_dir, "txt_processed/1-page_nb_cln")
    log_directory = os.path.join(output_directory, "logs")
    phrases_to_remove = ['Le danger d’y croire', 'Les Illuminés']
    titles_to_mark = [
        "Chapitre 1 Sous les projecteurs",
        "Chapitre 2 Au printemps comme en hiver",
        "Chapitre 3 Quand ça tourne... au vinaigre",
        "Chapitre 4 Le compas dans l'oeil",
        "Chapitre 5 Les étoiles qui pâlissent",
        "Chapitre 6 Là où on ne les attendait pas",
        "Chapitre 7 L'apparition",
        "Chapitre 8 L'oeil aveugle",
        "Chapitre 9 Rencontres au zénith",
        "Chapitre 10 Jour de repos",
        "Chapitre 11 Erreur sur la ligne",
        "Chapitre 12 Révélations",
        "Chapitre 13 Les plans secrets",
        "Chapitre 14 Retour à l'école",
        "Chapitre 15 Retrouvailles au sommet",
        "Chapitre 16 La convocation"
    ]

    process_directory(input_directory, output_directory, log_directory, phrases_to_remove, titles_to_mark)
    print("Script completed")
