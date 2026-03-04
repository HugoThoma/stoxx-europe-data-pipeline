/* SQL script to create the necessary tables for the Stoxx pipeline */


CREATE TABLE analytics_daily_returns AS
SELECT
    date,
    ticker,
    close,
    (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
    / LAG(close) OVER (PARTITION BY ticker ORDER BY date) /* For each ticker, sorted by date, take the last value of close and the current value of close to calculate the daily return */
        AS daily_return
FROM raw_prices
ORDER BY ticker, date;




/* Create the annualized returns table */
CREATE TABLE analytics_metrics AS
SELECT
    ticker,
    COUNT(*) AS nb_days,
    AVG(daily_return) * 252 AS annualized_return,
    STDDEV(daily_return) * SQRT(252) AS annualized_volatility /* ~252 trading days in a year */
FROM analytics_daily_returns
WHERE daily_return IS NOT NULL
GROUP BY ticker;
