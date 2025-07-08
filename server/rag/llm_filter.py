import logging

from utils.log_time import log_time

@log_time
def llm_chain_filter(docs, query, llm):
    """Filter documents based on relevance to the user's query using a language model.
    Args:
        docs (list): List of documents to filter.
        query (str): The user's query to check relevance against.
        llm: The language model used for filtering.
    Returns:
        list: Filtered list of documents that are relevant to the query.
    """

    logging.info("Filtering {len(docs)} documents for query: {query}")
    filtered = []
    for doc in docs:
        prompt = (
                    f"Given the user query: '{query}', is the following context relevant? "
                    f"Context: {doc.page_content}\n\nResponse with 'yes' or 'no'."
                 )
        response = llm(prompt).strip().lower()
        if response.startswith("yes"):
            logging.info(f"Is the context fetched for given user's query relevant? Yes")
            filtered.append(doc)
    logging.info(f"Filtered down to {len(filtered)} relevant documents.")
    return filtered