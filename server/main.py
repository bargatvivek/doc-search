from utils.logging import setup_logging
setup_logging()

import logging
import os

from mcp_instance import mcp
from utils.config import load_env_vars, validate_env

# -- Add these lines to ensure tools resgistration, else tools/list will not get detected --
import tools.upload
import tools.query
# ---------------------------


if __name__ == "__main__":
    # Load and validate environment variables
    config = load_env_vars()
    validate_env()

    os.makedirs(config['VECTORSTORE_DIR'], exist_ok=True)

    # Set up logging
    logging.info("Starting the doc-search mcp server.")

    mcp.run()