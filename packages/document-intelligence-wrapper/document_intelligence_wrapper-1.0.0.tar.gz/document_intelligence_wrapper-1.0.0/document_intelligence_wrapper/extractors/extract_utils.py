# document_intelligence_wrapper/extractors/extract_utils.py

import pandas as pd

def convert_table_json_to_markdown(table) -> str:
    """
    Converts a JSON representation of a table to a Markdown table format.

    Args:
        table (dict): The JSON representation of the table.

    Returns:
        str: The Markdown string of the table.
    """
    headers = []
    rows = []

    max_row = table['rowCount']
    max_col = table['columnCount']

    cell_matrix = [[''] * max_col for _ in range(max_row)]

    for cell in table['cells']:
        row_idx = cell['rowIndex']
        col_idx = cell['columnIndex']
        content = cell['content'].replace("\n", "")

        if 'columnSpan' in cell and cell['columnSpan'] > 1:
            for span in range(cell['columnSpan']):
                cell_matrix[row_idx][col_idx + span] = content
        else:
            cell_matrix[row_idx][col_idx] = content

    for row_idx, row in enumerate(cell_matrix):
        if any('kind' in cell and cell['kind'] == 'columnHeader' for cell in table['cells'] if cell['rowIndex'] == row_idx):
            headers.append(row)
        else:
            rows.append(row)

    combined_headers = []
    if headers:
        for col_idx in range(max_col):
            combined_header = '\n'.join([header_row[col_idx].strip() for header_row in headers if header_row[col_idx].strip()])
            combined_headers.append(combined_header)
    else:
        combined_headers = ['Column ' + str(i + 1) for i in range(max_col)]

    df = pd.DataFrame(rows, columns=combined_headers)
    df = df.dropna(how='all').reset_index(drop=True)
    markdown_text = df.to_markdown(index=False)
    return markdown_text

def extract_text_from_json(ocr_json,page_section,figure_associations):
    """
    Extracts text from a JSON representation of document pages.

    Args:
        ocr_json (dict): The JSON data containing paragraphs and tables.
        page_section (dict): The output structure defining which paragraphs, tables, and figures to extract.
        figure_associations (dict): A dictionary mapping figures to their associated paragraphs.

    Returns:
        tuple: A tuple containing dictionaries for page text, table text, and full document text.
    """
    # Initialize dictionaries and variables to store the text of each page, tables, and full document
    page_text_dict = {}
    table_text_dict = {}
    full_doc_text = []

    # Table counter to give unique IDs to tables
    table_counter = 1

    # Iterate through each page in the output
    for page_num, elements in page_section.items():
        # Initialize a list to store text for the current page
        page_text = []

        # Add page header to full_doc_text
        full_doc_text.append(f"Page Number {page_num}")

        # Iterate through each element in the current page
        for element in elements:
            # Check if the element is a paragraph
            if 'paragraphs' in element:
                # Extract the paragraph number from the element string
                para_num = int(element.split(' ')[1])
                # Get the paragraph content
                para_content = ocr_json['paragraphs'][para_num]['content']
                # Append the content of the paragraph to the page_text list
                page_text.append(para_content)
                # Also append to full_doc_text
                full_doc_text.append(para_content)

            # Check if the element is a table
            elif 'tables' in element:
                # Extract the table number from the element string
                table_num = int(element.split(' ')[1])
                # Get the table content using table_markdown function
                table_content = convert_table_json_to_markdown(ocr_json['tables'][table_num])
                # Append the result to the page_text list
                page_text.append(table_content)
                # Also append to full_doc_text
                full_doc_text.append(table_content)
                # Store table content in table_text_dict with a unique key
                table_text_dict[f"Table {table_counter}"] = table_content
                # Increment the table counter
                table_counter += 1
                
            elif 'figures' in element:
                int(figure_associations[element][0])
                # Get the paragraph content
                figure_associated_para = int(figure_associations[element][0])
                fig_content = ocr_json['paragraphs'][figure_associated_para]['content']
                # Append the content of the paragraph to the page_text list
                page_text.append(fig_content)
                # Also append to full_doc_text
                full_doc_text.append(fig_content)

        # Join the list items with a newline character and store it in the dictionary
        page_text_dict[page_num] = '\n\n'.join(page_text)

    # Join all full_doc_text items with newline characters for the complete document text
    full_doc_text_combined = '\n\n'.join(full_doc_text)

    return page_text_dict, table_text_dict, full_doc_text_combined