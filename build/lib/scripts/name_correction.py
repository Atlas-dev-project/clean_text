#!/usr/bin/env python3
import os
import spacy
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

# Load SpaCy French large model
nlp = spacy.load('fr_core_news_lg')

def extract_and_replace_names(text):
    doc = nlp(text)
    name_replacements = {
        'ez': 'ez', 'as': 'a', 'et': 'é', 'cer': 'cer', 'tier': 'tié', 'ault': 'o', 'ner': 'nèr',
        'ber': 'bèr', 'ars': 'ar', 'ère': 'èr', 'zier': 'zié', 'champ': 'chan', 'igny': 'ini',
        'nie': 'ni', 'ort': 'or', 'ard': 'ar', 'ières': 'ièr', 'aux': 'o', 'us': 'us',
        'ois': 'oi', 'is': 'i', 'ent': 'en', 'ert': 'èr', 'os': 'o', 'ot': 'o',
        'ah': 'a', 'ée': 'é', 'ès': 'è’sse', 'és': 'é', 'oix': 'oi', 'ets': 'et', 'ues': 'ue'
    }

    exception_names = [
        "Boris", "Paris", "Doris", "Elvis", "Curtis", "Travis", "Chris", "Dennis", "Francis", "Lewis","Mars","Julieet","Sébas","Sergent"
        "Otis", "Phyllis", "Harris", "Morris", "Ennis", "Amaris", "Claris", "Wallis", "Jamis", "Yanis",
        "Loris", "Ellis", "Anis", "Idris", "Euris", "Mavis", "Norris", "Tavis", "Maris", "Candis", "Jadis",
        "Farris", "Ferris", "Avis", "Alis", "Eddis", "Iris", "Janis", "Jarvis", "Karis", "Ladis",
        "Genesis", "Nelis", "Bris", "Chrys", "Daris", "Elis", "Eris", "Hollis", "Kelis", "Thais",
        "Vallis", "Aulis", "Aris", "Clematis", "Clovis", "Damaris", "Ignis", "Rufus", "Silas",
        "Achilles", "Cris", "Iris", "Myrtis", "Narcis", "Peris", "Tallis", "Yanis", "Siris", "Annis",
        "Chris", "Davis", "Bigfoot", "Bigfoots", "Ward",
        "Chavez", "Perez", "Gomez", "Martinez", "Vazquez", "Cortez", "Hernandez", "Juarez", "Lopez", "Mez",
        "Lucas", "Jonas", "Thomas", "Nicholas", "Elias", "Tobias", "Zacharias", "Silas", "Pascal", "Mathias"
    ]

    names = [ent.text for ent in doc.ents if ent.label_ == 'PER']
    unique_names = set(names)
    replaced_names = []
    log = {}

    for name in unique_names:
        if name in exception_names:
            continue  # Skip the replacement for exception names
        for suffix, replacement in name_replacements.items():
            if name.endswith(suffix):
                new_name = name[:-len(suffix)] + replacement
                text = text.replace(name, new_name)
                replaced_names.append(new_name)
                log[name] = new_name
                break

    return text, log

def process_text_file(input_file_path, output_file_path, log_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text, replacements_log = extract_and_replace_names(text)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for original, replacement in replacements_log.items():
            log_file.write(f"{original}: {replacement}\n")

if __name__ == "__main__":
    input_directory = os.path.join(base_dir, "txt_processed/8-s_back_")
    output_directory = os.path.join(base_dir, "txt_processed/9-names_correction")
    log_directory = os.path.join(output_directory, 'logs_')

    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(log_directory, exist_ok=True)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)
            log_file_name = f"log_{file_name}"
            log_file_path = os.path.join(log_directory, log_file_name)

            print(f"Processing {file_name}...")
            process_text_file(input_file_path, output_file_path, log_file_path)
            print(f"Processed file saved as {file_name}")
            print(f"Log saved as {log_file_name}")

    print("Script completed")
