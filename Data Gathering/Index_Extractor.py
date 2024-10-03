import json
import os
import PyPDF2

def extract_pdf_outline(pdf_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Accessing the outline/bookmarks
        try:
            outline = reader.outline
        except AttributeError:
            print("Outline not available in this PDF")
            return None

        # Create a dictionary to store the table of contents (bookmarks)
        toc_dict = {}

        def parse_outline(outline_items, parent_name=None, indent_level=0):
            for item in outline_items:
                if isinstance(item, list):
                    parse_outline(item, parent_name, indent_level + 1)  # Recursively handle nested outlines
                else:
                    title = item.title
                    page = reader.get_destination_page_number(item) + 1  # Pages are 0-indexed
                    if parent_name:
                        title = f"{parent_name} > {title}"  # Handling nested items
                    toc_dict[title] = {"page": page, "indent_level": indent_level}

        # Parse the outline/bookmarks
        parse_outline(outline)

        return toc_dict

def write_to_json(data, output_file):
    # Writing the dictionary to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Table of contents written to {output_file}")

# Usage example
pdf_file = "../Data/Harry_Potter_(www.ztcprep.com).pdf"
table_of_contents = extract_pdf_outline(pdf_file)

if table_of_contents:
    # Path to the JSON file
    json_output_file = "../Data/table_of_contents.json"
    # Write the extracted outline to a JSON file
    write_to_json(table_of_contents, json_output_file)
