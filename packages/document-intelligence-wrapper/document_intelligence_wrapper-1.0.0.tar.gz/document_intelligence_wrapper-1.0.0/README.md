# Document Intelligence Wrapper

## Overview

The `document_intelligence_wrapper` is a Python package that provides a wrapper around the Azure Document Intelligence API. It offers easy-to-use functions to extract structured data, including text and tables, from documents. This wrapper is designed to handle complex document structures, such as tables with merged cells, and convert the extracted data into Markdown format, which is particularly useful for Generative AI processes and other automated text-processing workflows.

## Features

- Document Intelligence Client Wrapper: Simplifies the initialization and interaction with the Azure Document Intelligence API.
- Text Extraction: Extracts paragraphs and text from documents, organizing them page-by-page.
- Table Extraction with Merged Cells Handling: Converts tables, including those with merged cells, from JSON format to Markdown format.
- Markdown Output: Generates Markdown-formatted tables and text for easy visualization and integration with other text-processing tools.
- Organizes Data by Page: Outputs text and tables organized by page number and element order.

## Installation

To use this package, ensure you have installed the necessary dependencies. You can install the required packages using pip by running the following command in your terminal:

```python
pip install azure-ai-documentintelligence==1.0.0b3
pip install pandas==2.2.2
```


## Usage

The primary function to use from this package is get_text_from_pdf_with_doc_intelligence. This function extracts text and tables from a PDF file and organizes them in a structured format. The DocumentIntelligenceClientWrapper class is used to simplify client initialization.


### Step-by-Step Guide

### 1.Initialize the Document Intelligence Client: Use the DocumentIntelligenceClientWrapper to create a client with your Azure endpoint and key.

### 2. Call the Function: Use get_text_from_pdf_with_doc_intelligence with the initialized client and the path to your PDF file.

```python
from document_intelligence_wrapper.document_intelligence_client import DocumentIntelligenceClientWrapper
from document_intelligence_wrapper.extractors.pdf_text_extractor import get_text_from_pdf_with_doc_intelligence

# Define your Azure endpoint and key
endpoint = "your-azure-endpoint"
key = "your-azure-key"

# Initialize the Document Intelligence Client using the wrapper
client_wrapper = DocumentIntelligenceClientWrapper(endpoint, key)
client = client_wrapper.get_document_intelligence_client()

# Define the path to your PDF file
pdf_file_path = "path/to/your/document.pdf"

# Extract text and table data from the PDF
page_text_dict, table_text_dict, full_doc_text_combined = get_text_from_pdf_with_doc_intelligence(client, pdf_file_path)

# Output the extracted text and table data
print("Page Text:", page_text_dict)
print("Table Text:", table_text_dict)
print("Full Document Text:", full_doc_text_combined)
```


## Handling Complex Tables with Merged Cells

The provided function is designed to handle tables with merged cells seamlessly. It uses a cell matrix to map each cell’s position, taking into account any column spans (merged cells), ensuring that data is correctly represented in the output Markdown table.

### Example
Consider a table with merged header cells:


```json
{
    "rowCount": 3,
    "columnCount": 4,
    "cells": [
        {"rowIndex": 0, "columnIndex": 0, "content": "Header 1", "columnSpan": 2},
        {"rowIndex": 0, "columnIndex": 2, "content": "Header 2", "columnSpan": 1},
        {"rowIndex": 1, "columnIndex": 0, "content": "Sub-header 1"},
        {"rowIndex": 1, "columnIndex": 1, "content": "Sub-header 2"},
        {"rowIndex": 1, "columnIndex": 2, "content": "Sub-header 3"},
        {"rowIndex": 1, "columnIndex": 3, "content": "Sub-header 4"},
        {"rowIndex": 2, "columnIndex": 0, "content": "Data 1"},
        {"rowIndex": 2, "columnIndex": 1, "content": "Data 2"},
        {"rowIndex": 2, "columnIndex": 2, "content": "Data 3"},
        {"rowIndex": 2, "columnIndex": 3, "content": "Data 4"}
    ]
}

```

```
| Header 1      | Header 1      | Header 2      |               |
|---------------|---------------|---------------|---------------|
| Sub-header 1  | Sub-header 2  | Sub-header 3  | Sub-header 4  |
| Data 1        | Data 2        | Data 3        | Data 4        |

```

A table with 3 rows and 4 columns can have headers that span multiple columns. Merged cells like these are handled by the wrapper to ensure accurate representation in the Markdown format.

## Error Handling

- Authentication Errors: Ensure your Azure endpoint and API key are correctly configured. If you encounter authentication issues, double-check your credentials.
- File Not Found: If the specified PDF file path is incorrect, you will receive a file not found error. Ensure the path is correct and the file exists.
- Unsupported Document Format: The package is designed to handle PDF documents. If other formats are used, it may result in unexpected behavior.


## Advantages

- Ease of Use: Simplifies interaction with the Azure Document Intelligence API.
- Flexibility: Handles various document structures, including complex table layouts with merged cells.
- Markdown Format: Produces outputs in Markdown, making it easy to integrate with other text-processing tools and workflows.
- Scalable and Maintainable: Well-structured code, ready for production environments, with proper logging and error handling.

## Future Enhancements

- Support for Other Formats: Extend support to handle different document types beyond PDFs.
- More Detailed Logging: Incorporate more granular logging for better traceability.
- Custom Table Styling: Allow customization of Markdown table styles based on user requirements.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or report issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


 pip install -e /Users/ankit/Desktop/Work/own/document_intelligence_wrapper
