import os
from dotenv import load_dotenv

def load_env_vars():
    """
    Load environment variables from a .env file.
    
    Returns:
        dict: Dictionary containing the loaded environment variables.
    """
    load_dotenv()
    
    return {
        'SERPER_API_KEY': os.getenv('SERPER_API_KEY'),
        'LLM_MODEL': os.getenv('LLM_MODEL', 'gpt-3.5-turbo'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
        'VECTORSTORE_DIR': os.getenv('VECTORSTORE_DIR', './vectorstore'),
        'TOP_K': int(os.getenv('TOP_K', 5)),
        'CHUNK_SIZE': int(os.getenv('CHUNK_SIZE', 500)),
        'CHUNK_OVERLAP': int(os.getenv('CHUNK_OVERLAP', 50))
    }
    
def validate_env():
    """
    Validate that all required environment variables are set.
    
    Raises:
        ValueError: If any required environment variable is missing.
    """
    env = load_env_vars()
    missing = [k for k, v in env.items() if v is None]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
     
    int_fields = ['TOP_K', 'CHUNK_SIZE', 'CHUNK_OVERLAP']
    for field in int_fields:
        if not isinstance(env[field], int):
            raise TypeError(f"{field} must be of type int, got {type(env[field]).__name__} instead.")