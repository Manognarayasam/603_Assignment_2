#My Date of Birth 1998-08-04

import re
import PyPDF2
import json
import os
from datetime import datetime

def clean_text(text):
    # Remove unwanted characters and footnotes
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Removes non-ASCII characters like �
    text = re.sub(r'www\.\S+', '', text)  # Removes URLs like 'www.ztcprep.com'
    text = re.sub(r'\s+', ' ', text)  # Replaces multiple spaces/newlines with a single space
    return text.strip()

def extract_pages_to_text(pdf_file, start_page, target_page_number, output_file, num_internal_pages=10):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        current_internal_page = None
        extracted_pages = 0
        inside_target_page = False

        with open(output_file, 'w', encoding='utf-8') as text_file:
            for page_num in range(start_page, len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()

                # Print the page content even if target page is not hit yet
                cleaned_content = clean_text(text)
                #print(f"Extracting content from PDF page {page_num + 1}: {cleaned_content}\n")
                text_file.write(cleaned_content + "\n")

                # Look for the internal "P a g e | X" pattern
                match = re.finditer(r"P\s*a\s*g\s*e\s*\|\s*(\d+)", text)
                page_segments = list(match)

                # Process 
                # each match found on the current PDF page
                for i, segment in enumerate(page_segments):
                    internal_page_number = int(segment.group(1))
                    
                    if current_internal_page is None or internal_page_number > current_internal_page:
                        current_internal_page = internal_page_number
                        print(f"Found internal page {current_internal_page} on PDF page {page_num + 1}")

                    # Once we find the target internal page, start extraction from here
                    if current_internal_page >= target_page_number:
                        content_after_marker = text[segment.end():] if i == 0 else text
                        cleaned_content = clean_text(content_after_marker)
                        if cleaned_content:
                            #print(f"Extracting cleaned content: {cleaned_content}\n")
                            text_file.write(cleaned_content + "\n")
                        inside_target_page = True  # Start extraction from this point

                # If we have started extracting, increment the count
                if inside_target_page:
                    extracted_pages += 1
                    if extracted_pages >= num_internal_pages:
                        print(f"Extracted {num_internal_pages} internal pages up to internal page {current_internal_page}.")
                        return

def generate_files(birth_date, birth_year, table_of_contents, pdf_file, output_folder):
    birth_month = birth_date.month
    book_number = (birth_month // 2) if birth_month >= 8 else birth_month
    book_key = f"Book {book_number}"

    # Find the book and its starting page in the TOC
    book_start_page = None
    for chapter, info in table_of_contents.items():
        if book_key in chapter:
            book_start_page = info['page']
            break
    
    if not book_start_page:
        print(f"Book corresponding to birth month {birth_month} not found.")
        return

    # Extract file1.txt based on birth date
    file1_internal_start_page = birth_date.day  # Using the birth date as the internal page number
    file1_output = os.path.join(output_folder, "file1.txt")
    extract_pages_to_text(pdf_file, book_start_page, file1_internal_start_page, file1_output)
    print(f"Extracted content for file1.txt starting from internal page {file1_internal_start_page}")

    # Extract file2.txt based on birth year (1 added for 2000 and beyond)
    file2_internal_start_page = (100 if birth_year >= 2000 else birth_year % 100)
    file2_output = os.path.join(output_folder, "file2.txt")
    extract_pages_to_text(pdf_file, book_start_page, file2_internal_start_page, file2_output)
    print(f"Extracted content for file2.txt starting from internal page {file2_internal_start_page}")

def main():
    # Load the table of contents from JSON
    toc_file = "../Data/table_of_contents.json"
    with open(toc_file, 'r') as json_file:
        table_of_contents = json.load(json_file)

    # Get user's birth date and year
    birth_date_input = input("Enter your birth date (YYYY-MM-DD): ")
    birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d")
    birth_year = birth_date.year

    # Path to PDF and output folder
    pdf_file = "../Data/Harry_Potter_(www.ztcprep.com).pdf"
    output_folder = "../Data"

    # Generate file1.txt and file2.txt
    generate_files(birth_date, birth_year, table_of_contents, pdf_file, output_folder)

if __name__ == "__main__":
    main()
