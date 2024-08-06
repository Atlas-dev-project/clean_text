import os
import subprocess
import time
import logging
import sys

# Add the base directory to the PYTHONPATH
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from config import base_dir, log_file_path  # Import the base directory and log file path

# List of subdirectories relative to the base directory
subdirectories = [
    "txt_processed/0-main_txt",
    "txt_processed/1-page_nb_cln",
    "txt_processed/2-chapter_split",
    "txt_processed/3-paragraph_fix",
    "txt_processed/4-numbers_replaced",
    "txt_processed/5-line-fix",
    "txt_processed/6-#@%_added_for_liasons",
    "txt_processed/6-5-es_ait_",
    "txt_processed/7-word_replacement_",
    "txt_processed/8-s_back_",
    "txt_processed/9-names_correction",
]

# Ensure the PDF_drop directory is correctly referenced
pdf_drop_directory = os.path.join(base_dir, "PDF_drop")

# List of Python scripts to run
script_paths = [
    "scripts/pdf_2_txt.py",
    "scripts/remove_pnum_hilight_title.py",
    "scripts/split_chapters.py",
    "scripts/clean_text.py",
    "scripts/replace_numbers.py",
    "scripts/fix_lines.py",
    "scripts/liaisons.py",
    "scripts/ent_ait_fix.py",
    "scripts/replace_words.py",
    "scripts/replace_special_chars.py",
    "scripts/name_correction.py"
]

def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

# Function to update shebangs
def update_shebang(script_path):
    with open(script_path, 'r') as file:
        lines = file.readlines()

    if lines[0].startswith('#!'):
        lines[0] = f'#!/usr/bin/env python3\n'
    else:
        lines.insert(0, f'#!/usr/bin/env python3\n')

    with open(script_path, 'w') as file:
        file.writelines(lines)

def update_all_shebangs(script_paths):
    for script_path in script_paths:
        update_shebang(script_path)

# Function to run a script and log its output
def run_script(script_path):
    start_time = time.time()
    logging.debug(f"Running script: {script_path}")
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    end_time = time.time()
    output = result.stdout.strip()
    errors = result.stderr.strip()

    logging.info(f"Finished running script: {script_path} in {end_time - start_time:.2f} seconds")
    logging.info(f"Output:\n{output}\n")
    if errors:
        logging.error(f"Errors:\n{errors}\n")

def delete_txt_files_in_subdirectories(base_directory, subdirectories):
    for subdir in subdirectories:
        for root, dirs, files in os.walk(os.path.join(base_directory, subdir)):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        logging.info(f"Deleted file: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_path}: {e}")

def ensure_directories_exist(base_directory, subdirectories):
    for subdir in subdirectories:
        dir_path = os.path.join(base_directory, subdir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logging.info(f"Created directory: {dir_path}")

def main():
    start_time = time.time()
    script_paths_abs = [os.path.join(os.getcwd(), script) for script in script_paths]

    # Set up logging
    setup_logging(log_file_path)

    # Ensure directories exist
    ensure_directories_exist(base_dir, subdirectories)

    # Delete .txt files in the specified subdirectories
    delete_txt_files_in_subdirectories(base_dir, subdirectories)

    # Update shebangs
    update_all_shebangs(script_paths_abs)

    # Run scripts sequentially
    for script_path in script_paths_abs:
        run_script(script_path)

    total_time = time.time() - start_time
    logging.info(f"Total time for all tasks: {total_time:.2f} seconds")
    print(f"Total time for all tasks: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
