#!/usr/bin/env python3
import json
import re
import os
import glob
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

def flatten_nested_json(nested_json):
    flat_dict = {}
    for key, value in nested_json.items():
        if isinstance(value, dict):
            flat_dict.update(value)
        else:
            flat_dict[key] = value
    return flat_dict

def replace_words_using_json(json_file, input_dir, output_dir, log_dir):
    # Load the content of the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        nested_word_pairs = json.load(file)

    # Flatten the nested JSON structure
    word_pairs = flatten_nested_json(nested_word_pairs)

    # Get all text files in the input directory
    txt_files = glob.glob(os.path.join(input_dir, '*.txt'))

    if not txt_files:
        print(f"No text files found in {input_dir}")
        return

    # Process each text file
    for input_file_txt in txt_files:
        print(f"\nProcessing file: {input_file_txt}\n")
        # Read the content of the text file
        with open(input_file_txt, 'r', encoding='utf-8') as file:
            content = file.read()

        # Track replaced words
        replaced_words = []

        # Replace words according to the pairs in the JSON file
        for word, replacement in word_pairs.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content, num_replacements = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
                replaced_words.append(f"{word} -> {replacement} (replaced {num_replacements} times)")
                print(f"Replaced {word} with {replacement}: {num_replacements} times")

        # Define the output file paths
        output_file_txt = os.path.join(output_dir, os.path.basename(input_file_txt))
        summary_file_txt = os.path.join(log_dir, os.path.basename(input_file_txt).replace('.txt', '_summary.txt'))

        # Write the modified content to a new text file
        with open(output_file_txt, 'w', encoding='utf-8') as file:
            file.write(content)

        # Write the summary of replaced words to a new text file
        with open(summary_file_txt, 'w', encoding='utf-8') as file:
            file.write(f"Original file: {os.path.basename(input_file_txt)}\n\n")
            file.write("Replaced words:\n")
            if replaced_words:
                file.write("\n".join(replaced_words) + "\n")
            else:
                file.write("No words were replaced.\n")

# Usage of the function
json_file = os.path.join(base_dir, 'words_dictionary/words_dictionary.json')
input_dir = os.path.join(base_dir, 'txt_processed/6-5-es_ait_')
output_dir = os.path.join(base_dir, 'txt_processed/7-word_replacement_')
log_dir = os.path.join(output_dir, 'logs')

# Create the output and log directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

replace_words_using_json(json_file, input_dir, output_dir, log_dir)
