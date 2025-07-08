import logging

from utils.log_time import log_time

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

@log_time
def create_vector_store(chunks, persist_directory, embedding_model):
    """
    Create a vectorstore from the provided chunks and persist it to the specified directory.
    
    Args:
        chunks (list): List of text chunks to be indexed.
        persist_directory (str): Directory where the vectorstore will be persisted.
        embedding_model (str): Model to be used for embeddings.
        
    Returns:
        Chroma: A Chroma vectorstore instance.
    """
    
    logging.info(f"Creating vectorstore with {len(chunks)} chunks at {persist_directory} using model {embedding_model}")
    embeddings = OllamaEmbeddings(model=embedding_model)

    try:
        batch_size = 20
        vectorstore = None
        total_batches = (len(chunks) + batch_size - 1) // batch_size
        for batch_num, i in enumerate(range(0,  len(chunks), batch_size), start=1):

            batch = chunks[i:i + batch_size]
            logging.info(f"Processing batch {batch_num}/{total_batches} with {len(batch)} chunks.")

            if vectorstore is None:
                vectorstore = Chroma.from_documents(batch, embeddings, persist_directory=persist_directory)
                logging.info(f"Created vectorstore with initial batch of {len(batch)} chunks.")
            else:
                vectorstore.add_documents(batch)
                vectorstore.persist()
            logging.info(f"Added batch {batch_num} to vectorstore and persisted.")

        logging.info(f"Vector store created and persisted.")

        return vectorstore
    except Exception as e:
        logging.error(f"Failed to create vectorstore: {e}")
        raise RuntimeError(f"Failed to create vectorstore: {e}")