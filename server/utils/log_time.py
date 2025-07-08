import logging
import time

def log_time(func):
    """
    Decorator to log the execution time of a function.
    
    Args:
        func (callable): The function to be decorated.
        
    Returns:
        callable: The wrapped function with logging.
    """
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Function '{func.__name__}' executed in {elapsed_time:.3f} seconds")
        return result
    
    return wrapper