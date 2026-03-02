from src.logging_config import setup_logging
import logging

###
#
# This is the main entry point for the stoxx_pipeline project. 
# It imports the logging configuration from the logging_config module and sets up logging for the pipeline. 
# The logger is then used to log an informational message indicating that the pipeline has started.
#
###


setup_logging()

logger = logging.getLogger(__name__)

logger.info("Pipeline started")