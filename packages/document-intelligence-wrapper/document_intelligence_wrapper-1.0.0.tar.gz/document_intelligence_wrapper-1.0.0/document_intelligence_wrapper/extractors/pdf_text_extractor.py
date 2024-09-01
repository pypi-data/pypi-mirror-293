# document_intelligence_wrapper/extractors/pdf_text_extractor.py

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat, AnalyzeResult
from document_intelligence_wrapper.extractors.document_processor import process_document
from document_intelligence_wrapper.extractors.extract_utils import extract_text_from_json

def get_text_from_pdf_with_doc_intelligence(client, pdf_file_path: str) -> dict:
    """
    Extracts text from a PDF file using Azure Document Intelligence and processes the result.

    Args:
        client (DocumentIntelligenceClient): The Azure Document Intelligence client.
        pdf_file_path (str): The file path to the PDF document.

    Returns:
        dict: A dictionary where keys are page numbers and values are lists of element identifiers in order.
    """
    with open(pdf_file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            analyze_request=f,
            output_content_format=ContentFormat.MARKDOWN,
            content_type="application/octet-stream",
        )
    ocr_json: AnalyzeResult = poller.result()
    ocr_json = poller.result()
    # Call the process_document function to process the result
    page_section,figure_associations = process_document(ocr_json)

    page_text_dict, table_text_dict, full_doc_text_combined = extract_text_from_json(ocr_json,page_section,figure_associations)

    return page_text_dict, table_text_dict, full_doc_text_combined
