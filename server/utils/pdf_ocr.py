import logging

from utils.log_time import log_time

from langchain_community.document_loaders import PDFPlumberLoader

@log_time
def load_pdf_with_ocr(file_path: str) -> list:
    """
    Load a PDF file and perform OCR on its pages.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        list: List of text content extracted from each page of the PDF.
    """
    
    logging.info(f"Loading PDF file with OCR: {file_path}")
    
    try:
        loader = PDFPlumberLoader(file_path, extract_images=True)
        documents = loader.load()
        logging.info(f"Loaded {len(documents)} pages from the PDF.")
        
        return [doc.page_content for doc in documents]
    
    except Exception as e:
        logging.error(f"Error loading PDF with OCR: {e}")
        raise   