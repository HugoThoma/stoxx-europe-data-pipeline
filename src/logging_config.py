import logging
import os


###
# 
# This module sets up logging for the stoxx_pipeline project. 
# It configures logging to output both to a file and to the console, 
# with a specific format that includes the timestamp, log level, logger name, and message. 
# The log files are stored in a "logs" directory.
#
###
def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler()
        ]
    )