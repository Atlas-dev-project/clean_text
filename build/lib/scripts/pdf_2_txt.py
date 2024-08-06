#!/usr/bin/env python3
import os
import pdfplumber
import re
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

def clean_text(text):
    # Define the unwanted text pattern with a regex that matches the specified format
    unwanted_pattern = re.compile(
        r''
    )
    
    # Remove the unwanted text
    text = unwanted_pattern.sub('', text)
    
    # Additional cleaning to handle multiple consecutive spaces left after removal
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Remove any leading or trailing whitespace
    text = text.strip()
    
    return text

def extract_text_from_pdf(pdf_path, output_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                page_text = clean_text(page_text)
                print(f"Extracted text from page {page_num}:\n{page_text}\n{'-'*40}\n")
                text += page_text + "\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def process_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.pdf'):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_name = f'{os.path.splitext(file_name)[0]}.txt'
            output_file_path = os.path.join(output_directory, output_file_name)

            print(f"Processing {file_name}...")
            extract_text_from_pdf(input_file_path, output_file_path)
            print(f"Processed file saved as {output_file_name}")

if __name__ == "__main__":
    input_directory = os.path.join(base_dir, 'PDF_drop')
    output_directory = os.path.join(base_dir, 'txt_processed/0-main_txt')

    process_directory(input_directory, output_directory)
    print("Script completed")
