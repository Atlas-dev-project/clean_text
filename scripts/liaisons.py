#!/usr/bin/env python3
import spacy
import os
import datetime
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from config import base_dir  # Import the base directory

# Load the French language model in SpaCy
nlp = spacy.load("fr_core_news_lg")

# Directory paths
input_dir = os.path.join(base_dir, 'txt_processed/5-line-fix')
output_dir = os.path.join(base_dir, 'txt_processed/6-#@%_added_for_liasons')
log_dir = os.path.join(output_dir, "logs")

# Ensure output and log directories exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# List of exceptions for liaisons with "s"
exceptions_s = {
    "et", "ou", "en", "à", "de", "par", "sans", "très", "plus", "trop", "moins", "peu",
    "ne", "je", "me", "te", "se", "que", "ce", "pas", "sur", "sous", "dans", "chez",
    "ici", "oui", "or", "où", "leur", "tout", "bien", "fort", "sauf",
    "au", "aux", "allait", "avait", "aussi", "ai", "ait", "sais", "vois",
    "il", "elle", "on", "vis", "dis", "pis", "lis", "mis","ris", "lis",
    "un", "une", "après", "autrement", "autrefois", "avec", "ont", "avaient",
    "entra", "ha", "hé", "hi", "ho", "hu",
    "les", "des", "mes", "ses", "ces", "tes", "nos", "vos", "leurs", "nous", "vous",
    "viens", "lesquels", "fils", "a", "-vous", "puis", "fois", "fus", "mais", "vais",
    "a", "as", "hôtes", "jamais", "mots", "poses", "suis", "jours", "temps", "toujours",
    "depuis", "gens"
}

# Function to identify and replace liaisons
def identify_and_replace_liaisons(text):
    doc = nlp(text)
    liaisons = []
    modified_tokens = []

    replacements = {
        "é'tun": 0,
        "ét'une": 0,
        "é't": 0,
        "cét'un": 0,
        "cét'une": 0,
        "cé't": 0,
        "n'ét'un": 0,
        "n'ét'une": 0,
        "né't": 0,
        "#@%": 0,
        "ils#@%": 0,
        "elles#@%": 0
    }

    i = 0
    while i < len(doc) - 1:
        token = doc[i]
        next_token = doc[i + 1]
        word = token.text

        # Skip processing for proper nouns
        if token.pos_ == 'PROPN':
            word = token.text
        # Apply specific rules for "est" first to avoid overlap
        elif token.text == "est":
            if next_token.text == "un":
                word = "ét'un"
                liaisons.append((token.text, next_token.text, word))
                replacements["é'tun"] += 1
                i += 1  # Skip next token
            elif next_token.text == "une":
                word = "ét'une"
                liaisons.append((token.text, next_token.text, word))
                replacements["ét'une"] += 1
                i += 1  # Skip next token
            elif next_token.text[0] in 'aeiouhéà':
                word = "é't"
                liaisons.append((token.text, next_token.text, word))
                replacements["é't"] += 1
            else:
                word = token.text
        elif token.text == "c'est":
            if next_token.text == "un":
                word = "cét'un"
                liaisons.append((token.text, next_token.text, word))
                replacements["cét'un"] += 1
                i += 1  # Skip next token
            elif next_token.text == "une":
                word = "cét'une"
                liaisons.append((token.text, next_token.text, word))
                replacements["cét'une"] += 1
                i += 1  # Skip next token
            elif next_token.text[0] in 'aeiouhéà':
                word = "cé't"
                liaisons.append((token.text, next_token.text, word))
                replacements["cé't"] += 1
            else:
                word = token.text
        elif token.text == "n'est":
            if next_token.text == "un":
                word = "n'ét'un"
                liaisons.append((token.text, next_token.text, word))
                replacements["n'ét'un"] += 1
                i += 1  # Skip next token
            elif next_token.text == "une":
                word = "n'ét'une"
                liaisons.append((token.text, next_token.text, word))
                replacements["n'ét'une"] += 1
                i += 1  # Skip next token
            elif next_token.text[0] in 'aeiouhéà':
                word = "né't"
                liaisons.append((token.text, next_token.text, word))
                replacements["né't"] += 1
            else:
                word = token.text
        # Apply specific rule for "qu'" + "ils"/"elles"
        elif token.text == "qu'" and next_token.text in {"ils", "elles"}:
            word = "qu'#@%" + next_token.text[1:]
            liaisons.append((token.text, next_token.text, word))
            replacements["#@%"] += 1
        # Apply general rules for liaisons with "s" for "ils" and "elles"
        elif token.text in {"ils", "elles"} and next_token.text[0] in 'aeiouh':
            word = token.text[:-1] + "#@%"
            liaisons.append((token.text, next_token.text, word))
            replacements[token.text + "#@%"] += 1
        # Apply general rules for liaisons with "s"
        elif token.text.endswith('s') and next_token.text[0] in 'aeiouhàé' and token.text.lower() not in exceptions_s and next_token.text.lower() not in exceptions_s:
            word = token.text[:-1] + "#@%"
            liaisons.append((token.text, next_token.text, "#@%"))
            replacements["#@%"] += 1
        # Apply general rules for other cases
        else:
            word = token.text
        
        modified_tokens.append(word + token.whitespace_)
        i += 1

    # Append the last token
    modified_tokens.append(doc[-1].text + doc[-1].whitespace_)

    return liaisons, ''.join(modified_tokens), replacements

# Process each file
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            # Identify and replace liaisons in the text
            liaisons, modified_text, replacements = identify_and_replace_liaisons(text)
            
            # Create a log for the file
            log_file_path = os.path.join(log_dir, f"{filename}_log.txt")
            with open(log_file_path, 'w', encoding='utf-8') as log_file:
                log_file.write(f"File: {filename}\n\n")
                for liaison in liaisons:
                    log_file.write(f"{liaison[0]} - {liaison[1]} replaced by {liaison[2]}\n")
                log_file.write("\nReplacement counts:\n")
                for key, value in replacements.items():
                    log_file.write(f"{key}: {value}\n")

            # Write the modified text to output file
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(modified_text)
        except Exception as e:
            error_log_path = os.path.join(log_dir, f"{filename}_error_log.txt")
            with open(error_log_path, 'w', encoding='utf-8') as error_log:
                error_log.write(f"Error processing file: {filename}\n")
