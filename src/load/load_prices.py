from sqlalchemy import text
from src.db.database import get_db_engine
import logging

logger = logging.getLogger(__name__)


###
# This module is responsible for loading the extracted price data into the database.
# Input: A DataFrame containing the companies' stock prices with columns: 
#   date, ticker, open, high, low, close, volume.
# Output: The data is inserted into the raw_prices table in the database.
###
def load_prices(df):

    if df.empty:
        logger.warning("No data to load")
        return

    engine = get_db_engine()

    with engine.begin() as connection:

        for _, row in df.iterrows():

            query = text("""
            INSERT INTO raw_prices
            (ticker, date, open, high, low, close, volume)
            VALUES
            (:ticker, :date, :open, :high, :low, :close, :volume)
            ON CONFLICT (ticker, date) DO NOTHING
            """)

            connection.execute(query, row.to_dict())

    logger.info("Data loaded successfully")