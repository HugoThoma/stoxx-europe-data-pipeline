CREATE TABLE IF NOT EXISTS raw_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* Add a unique constraint to ensure that each ticker has only one entry per date */
ALTER TABLE raw_prices
ADD CONSTRAINT unique_ticker_date UNIQUE (ticker, date);


/* Create an index on the ticker and date columns to improve query performance */
/* B-Tree index is the default and is suitable for this use case */
CREATE INDEX IF NOT EXISTS idx_raw_prices_ticker_date
ON raw_prices (ticker, date);