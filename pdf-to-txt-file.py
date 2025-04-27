from pdfminer.high_level import extract_text
import re
import os

folder_path = './data'

def pdf_to_txt(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF

    Parameters:
    pdf_path (str): The path to the PDF file from which to extract text.

    Returns:
    None: Outputs the extracted text to a .txt file.
    """
    # Extract text using pdfminer
    text = extract_text(pdf_path)

    processed_text = remove_unneeded_lines(text)
    processed_text = normalize_paragraph_spacing(processed_text)
    processed_text = remove_all_single_lines(processed_text)

    # Write the processed text to a file
    with open(pdf_path.replace('.pdf', '_extracted.txt'), 'w', encoding='utf-8') as f_out:
        f_out.write(processed_text)

def remove_unneeded_lines(text):
    # delete urls, emails, ...
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'\S+@\S+|'
        r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|'
        r'^\s*[\-+]?[0-9]+\.?[0-9]*\s*$|'
        r'\.com\b|'
        r'\bISSN\b|'
        r'\bJournal\b|'
        r'\bDOI\b|'
        r'Vol\s+\d+|'
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b|'
        r'downloaded\s+from\s*',
        re.IGNORECASE  # Ignoriere Groß-/Kleinschreibung
    )
    
    # delete lines with special characters
    pattern_non_alpha_numeric = re.compile(r'^[^a-zA-Z0-9]+$')
    
    # delete short lines with max 10 characters
    pattern_short_lines = re.compile(r'^.{1,10}$')
    
    cleaned_lines = []
    for line in text.split('\n'):
        if line.strip() == "":
            cleaned_lines.append(line)
        if not pattern.search(line) and not pattern_non_alpha_numeric.search(line) and not pattern_short_lines.search(line):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def normalize_paragraph_spacing(text):
    #integrate seperator for paragraph separation
    normalized_text = re.sub(r'\n\s*\n+', '\n\n<newParagraph>\n', text)
    return normalized_text

def remove_all_single_lines(text):
    """
    removes all paraghraphs with just one line
    """
    paragraphs = text.split('<newParagraph>\n')
    filtered_paragraphs = []

    for paragraph in paragraphs:
        if paragraph.count('\n') > 2:
            filtered_paragraphs.append(paragraph)

    return '<newParagraph>\n'.join(filtered_paragraphs)

# iterate through all pdf files in a given folder_path and convert them into processed txt files
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(folder_path, filename)
        pdf_to_txt(pdf_path)





    