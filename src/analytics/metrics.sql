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




SELECT
    ticker,
    company_score,
    RANK() OVER (ORDER BY company_score DESC) AS rank
FROM (
    SELECT
        ticker,
        (
            sharpe_ratio * 0.6 +
            annualized_return * 0.3 +
            max_drawdown * 0.1
        ) AS company_score
    FROM analytics_metrics
) s;