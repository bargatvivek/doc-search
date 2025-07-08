import logging

def setup_logging():
    """
    Set up logging configuration for the application.
    
    This function configures the logging to output messages to the console with a specific format.
    The log level is set to INFO, which means all messages at this level and above will be logged.
    """
    logging.basicConfig(
        filename='doc-search.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    