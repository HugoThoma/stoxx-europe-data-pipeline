Select count(*) from public.raw_prices;

/*
SELECT *
FROM raw_prices
ORDER BY date DESC
LIMIT 10;
*/

/* Business performance analysis */
/*
SELECT ticker,
       MIN(date) as first_date,
       MAX(date) as last_date,
       COUNT(*) as nb_days
FROM raw_prices
GROUP BY ticker;
*/

/* 1-year performance */
/*
SELECT ticker,
       (MAX(close) - MIN(close)) / MIN(close) * 100 AS performance_pct
FROM raw_prices
GROUP BY ticker;
*/

/* Real 1-year performance */
SELECT ticker,
       (last_close - first_close) / first_close * 100 AS performance_pct
FROM (
    SELECT ticker,
           FIRST_VALUE(close) OVER w AS first_close,
           LAST_VALUE(close) OVER w AS last_close
    FROM raw_prices
    WINDOW w AS (PARTITION BY ticker ORDER BY date
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
) t
GROUP BY ticker, first_close, last_close;

/* volatility */
/*
SELECT ticker,
       STDDEV(close) as volatility
FROM raw_prices
GROUP BY ticker;
*/

