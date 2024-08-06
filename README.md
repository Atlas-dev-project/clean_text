# EBook Processor

This project processes PDF files through various scripts to extract, clean, format and export text from a PDF file

## Folder Structure

`scripts/`: Contains the processing scripts.

`words_dictionary/`: Contains the JSON file with words and their replacements.  This is where you will add words that you want to be replaced in the extracted text

`txt_processed/`: Contains the processed text files OUTPUT in various stages.

`PDF_drop/`: Is where you put the PDF you want to extract and format the text from.  The PDF file has to be dropped in this folder before running main.py script



# How to Use

1. **Clone the repository to your local machine**.
   In terminal insert :
                        git clone /path/to/your/repository
   
2. **Insert your BASE DIRECTROY**
   Inside the file ; `config.py`: You cand edit you directory path and insert it in YOUR path directory inside the quotes.  (ex base_dir = "your/path/directory") 

3. **Navigate to the project directory**.
   In terminal insert :
   cd /Volumes/your/path/directory  

4. **Create and activate a virtual environment**.
    In terminal insert : 
                         python3 -m venv venv
                         source venv/bin/activate

5. Place your PDF file in the `PDF_drop` directory.

6. Make the shell script executable, run the following command:
   In terminal insert : 
                         chmod +x run_processor.sh

3. Run the processing script. You can use the provided shell script to
   automate this process:
   In terminal insert : 
                         ./run_processor.sh
