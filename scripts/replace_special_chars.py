#!/usr/bin/env python3
import os
import re
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

# Directory paths
input_dir = os.path.join(base_dir, "txt_processed/7-word_replacement_")
output_dir = os.path.join(base_dir, "txt_processed/8-s_back_")
log_dir = os.path.join(output_dir, "logs")

# Ensure the output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Function to process each file and replace occurrences
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find and replace all occurrences of #@%
    replacements = {
        r'#@%': 's'
    }
    
    replaced_words = []
    
    for pattern, replacement in replacements.items():
        occurrences = re.findall(pattern, content)
        if occurrences:
            replaced_words.extend([(occurrence, replacement) for occurrence in occurrences])
            content = re.sub(pattern, replacement, content)
    
    # Write the processed content to a new file
    output_file_path = os.path.join(output_dir, os.path.basename(file_path).replace(".txt", "_processed.txt"))
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Log the replacements
    if replaced_words:
        log_file_path = os.path.join(log_dir, os.path.basename(file_path).replace(".txt", "_log.txt"))
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"File: {os.path.basename(file_path)}\n")
            for old, new in replaced_words:
                log_file.write(f"Replaced: {old} with '{new}'\n")
            log_file.write("\n")

# Process each .txt file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt") and not filename.endswith("_processed.txt"):
        file_path = os.path.join(input_dir, filename)
        process_file(file_path)

print("Processing complete.")
