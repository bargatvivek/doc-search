import logging

from utils.log_time import log_time
from utils.config import load_env_vars

from langchain_community.utilities import GoogleSearchAPIWrapper

config = load_env_vars()

@log_time
def web_search(query):
    """
    Perform a web search using the Google Search API.
    
    Args:
        query (str): The user's query to search for.
        
    Returns:
        list: List of search results from the web.
    """
    
    logging.info(f"Performing web search for query: {query}")
    
    if not config['SERPER_API_KEY']:
        logging.error("SERPER_API_KEY is not set in the environment variables.")
        raise ValueError("SERPER_API_KEY is required for web search functionality.")

    search = GoogleSearchAPIWrapper(api_key=config['SERPER_API_KEY'])
    results = search.run(query)
    logging.info(f"Web search completed")
    return results