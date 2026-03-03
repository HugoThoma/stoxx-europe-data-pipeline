from src.logging_config import setup_logging
from src.extract.fetch_prices import fetch_prices
from src.load.load_prices import load_prices
###
#
# This is the main entry point for the stoxx_pipeline project. 
# It imports the logging configuration from the logging_config module and sets up logging for the pipeline. 
# The logger is then used to log an informational message indicating that the pipeline has started.
#
###


def main():

    setup_logging()

    df = fetch_prices(period="1y")
    load_prices(df)

if __name__ == "__main__":
    main()