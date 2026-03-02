from sqlalchemy import text
from src.db.database import get_db_engine
from src.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


###
#
# Initializes the database by executing the SQL schema defined in 'src/models/raw_schema.sql'.
#
###
def init_database():
    engine = get_db_engine()

    with open("src/models/raw_schema.sql", "r") as file:
        schema_sql = file.read()

    with engine.connect() as connection:
        connection.execute(text(schema_sql))
        connection.commit()

    logger.info("Database schema initialized successfully.")

if __name__ == "__main__":
    init_database()