import logging

from utils.log_time import log_time
from utils.config import load_env_vars

config = load_env_vars()

@log_time
def rerank_documents(docs, query, llm, top_k=config['TOP_K']):
    """
    Rerank documents based on their relevance to the user's query using a language model.
    
    Args:
        docs (list): List of documents to rerank.
        query (str): The user's query to check relevance against.
        llm: The language model used for reranking.
        top_k (int): Number of top documents to return after reranking.
        
    Returns:
        list: Reranked list of documents that are most relevant to the query.
    """
    
    logging.info(f"Reranking {len(docs)} documents for query: {query}")

    if not docs:
        logging.info("No documents to rerank.")
        return []
    prompt = [
        f"Given the query: '{query}', rate the relevance of the following context: \n\n {doc.page_content}\n\n Score (0-10):"
        for doc in docs
    ]

    scores = []
    for prompt, doc in zip(prompt, docs):
        try:
            score_str = llm(prompt).strip()
            score = int(''.join(filter(str.isdigit, score_str)))
        except Exception as e:
            logging.warning(f"Failed to get score from LLM: {e}")
            score = 0   
        scores.append((score, doc))

    reranked = [doc for score, doc in sorted(scores, key=lambda x: x[0], reverse=True)]
    logging.info(f"Reranked and selected top {top_k} documents based on LLM scores.")
    return reranked[:top_k] if len(reranked) > top_k else reranked
    