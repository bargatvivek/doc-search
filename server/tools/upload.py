import logging
import os

from datetime import datetime, timezone
from mcp_instance import mcp
from typing import List
from utils.log_time import log_time
from utils.chunking import semantic_chunker, split_documents
from utils.config import load_env_vars
from utils.pdf_ocr import load_pdf_with_ocr
from utils.vectorstore import create_vector_store

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.document_loaders import Docx2txtLoader

config = load_env_vars()

@log_time
@mcp.tool()
def upload(filepaths: List[str], meta_data: dict) -> str:
    """
    Upload and index PDF, TXT, or DOCX files for retrieval.
    filepaths: List of file paths to upload.
    meta_data: Metadata to associate with the uploaded documents.
    eg:
        meta_data = {
            "identifier": "unique_identifier"
        }
    Returns:
        str: Confirmation message indicating successful upload and indexing of documents.
    """

    logging.info(f"\n========================================================================================\n")
    logging.info(f"Upload tool called with filepaths: {filepaths} and meta_data: {meta_data}")

    if not filepaths or not meta_data or "identifier" not in meta_data:

        logging.error("No filepaths provided or identifier missing in meta_data.")
        return "Filepaths and meta_data with identifier are required."


    all_chunks = []
    utc_now = datetime.now(timezone.utc).isoformat()
    identifier = meta_data.get("identifier", "")

    vectorstore = Chroma(
        persist_directory=config['VECTORSTORE_DIR'],
        embedding_function=OllamaEmbeddings(model=config['EMBEDDING_MODEL'])
    )
    where = {"identifier": identifier}
    ids_to_delete = vectorstore._collection.get(where=where).get("ids", [])
    deleted_count = len(ids_to_delete)
    vectorstore.delete(where=where)
    logging.info(f"Deleted {deleted_count} existing documents with identifier: {identifier}")

    for filepath in filepaths:
        ext = os.path.splitext(filepath)[1].lower()
        file_name = os.path.basename(filepath)
        doc_metadata = {
            "file_name": file_name,
            "file_path": filepath,
            "identifier": identifier,
            "upload_time": utc_now
        }
        if ext == ".pdf":
            logging.info(f"Processing PDF file: {file_name}")
            docs = load_pdf_with_ocr(filepath)
        elif ext == ".txt":
            logging.info(f"Processing TXT file: {file_name}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            docs = [Document(page_content=content, metadata={"source": filepath})]
        elif ext == ".docx":
            logging.info(f"Processing DOCX file: {file_name}")
            loader = Docx2txtLoader(filepath)
            docs = loader.load()
        else:
            logging.error(f"Unsupported file type: {ext} for file: {file_name}")
            return "Only PDF, TXT, and DOCX files are supported."
        
        sem_chunks = semantic_chunker(docs)
        split_chunks = split_documents(sem_chunks, chunk_size=config['CHUNK_SIZE'], chunk_overlap=config['CHUNK_OVERLAP'])

        # logging.info(f"Splitted {file_name} into {len(split_chunks)} chunks with size {config['CHUNK_SIZE']} and overlap {config['CHUNK_OVERLAP']}.")

        for chunk in split_chunks:
            if not hasattr(chunk, 'metadata') or chunk.metadata is None:
                chunk.metadata = {}
            chunk.metadata.update(doc_metadata)
            logging.info(f"File: {file_name} | Chunk {split_chunks.index(chunk)+1}:\n{chunk}\n")
        
        logging.info(f"Splitted {file_name} into {len(split_chunks)} chunks.")
        all_chunks.extend(split_chunks)

    create_vector_store(all_chunks, persist_directory=config['VECTORSTORE_DIR'], embedding_model=config['EMBEDDING_MODEL'])

    logging.info(f"Documents uploaded and indexed successfully with identifier: {identifier}")
    logging.info(f"\n========================================================================================\n")
    return f"Documents uploaded and indexed successfully with identifier: {identifier}"