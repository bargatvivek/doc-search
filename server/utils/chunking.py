import logging

from utils.log_time import log_time

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

@log_time
def semantic_chunker(documents):
    """
    Chunk a list of documents into smaller pieces for processing.
    
    Args:
        documents (list): List of Document objects to be chunked.
        
    Returns:
        list: List of chunked Document objects.
    """
    
    logging.info(f"Semantic chunking {len(documents)} documents")

    # 1. Paragraph-based chunking:
    # Split documents into paragraphs (or smaller sections) based on newlines or other delimiters.

    # 2. Heading-based chunking:
    # If your document have heading (like Markdown or DOCX), you can split based on headings.

    # 3. Semantic chunking:
    # Use a sentence tokenizer (eg: from NLTK or SpaCy) to split documents into sentences, then group sentences into chunks based on semantic similarity.

    # 4. Custom chunking:
    # Use a LLM or keyword-based approach to find topic boundaries and chunk documents accordingly.
    
    return documents

@log_time
def split_documents(documents, chunk_size, chunk_overlap):
    logging.info(f"Splitting {len(documents)} documents into chunks of size {chunk_size} with overlap {chunk_overlap}")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    docs = [Document(page_content=doc) if isinstance(doc, str) else doc for doc in documents]
    return splitter.split_documents(docs)