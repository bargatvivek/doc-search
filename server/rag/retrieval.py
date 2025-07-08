import logging

from utils.log_time import log_time
from utils.config import load_env_vars

config = load_env_vars()

@log_time
def get_retriever(vectorstore, top_k=config['TOP_K'], metadata_filter=None):
    """
    Create a retriever from the vectorstore with optional metadata filtering.
    
    Args:
        vectorstore: The vectorstore to create the retriever from.
        top_k (int): Number of top documents to return.
        metadata_filter (dict, optional): Metadata to filter documents by.
        
    Returns:
        retriever: A retriever object configured with the vectorstore and filters.
    """
    
    logging.info(f"Creating retriever with top_k={top_k} and metadata_filter={metadata_filter}")
    
    search_kwargs = {"k": top_k}

    if metadata_filter:
        search_kwargs["filter"] = metadata_filter
    return vectorstore.as_retriever(search_kwargs=search_kwargs)