from sqlalchemy import text
from src.db.database import get_db_engine


def compute_daily_returns():
    engine = get_db_engine()

    query = text("""
        DROP TABLE IF EXISTS analytics_daily_returns;

        CREATE TABLE analytics_daily_returns AS
        SELECT
            date,
            ticker,
            close,
            prev_close,
            (close - prev_close) / prev_close AS daily_return
        FROM (
            SELECT
                date,
                ticker,
                close,
                LAG(close) OVER (
                    PARTITION BY ticker
                    ORDER BY date
                ) AS prev_close
            FROM raw_prices
        ) t
        ORDER BY ticker, date;
    """)

    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()

###
# This module compute annualized metrics.
# WITH allows to break the query into 2 steps: 
# 1. Compute the returns stats (average return, volatility, min/max close) for each ticker
# 2. Compute the min drawdown for each ticker
# 3. Join the results to get the final analytics metrics for each ticker.
###
def compute_analytics_metrics():
    engine = get_db_engine()

    query = text("""
        DROP TABLE IF EXISTS analytics_metrics;

        CREATE TABLE analytics_metrics AS
        WITH returns_stats AS (
            SELECT
                ticker,
                COUNT(*) AS nb_days,
                AVG(daily_return) * 252 AS annualized_return,
                STDDEV(daily_return) * SQRT(252) AS annualized_volatility,
                MIN(close) AS min_close,
                MAX(close) AS max_close
            FROM analytics_daily_returns
            WHERE daily_return IS NOT NULL
            GROUP BY ticker
        ),
        drawdown_calc AS (
            SELECT
                ticker,
                MIN(drawdown) AS max_drawdown
            FROM (
                SELECT
                    ticker,
                    date,
                    close,
                    close /
                        MAX(close) OVER (
                            PARTITION BY ticker
                            ORDER BY date
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) - 1 AS drawdown
                FROM analytics_daily_returns
            ) dd
            GROUP BY ticker
        )
        SELECT
            r.ticker,
            r.nb_days,
            (r.max_close / r.min_close - 1) AS total_return,
            r.annualized_return,
            r.annualized_volatility,
            (r.annualized_return / NULLIF(r.annualized_volatility, 0)) AS sharpe_ratio,
            d.max_drawdown
        FROM returns_stats r
        JOIN drawdown_calc d
            ON r.ticker = d.ticker;
    """)

    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()

###
# This module computes the analytics metrics based on the raw price data.
###
def rebuild_analytics_layer():
    compute_daily_returns()
    compute_analytics_metrics()








# def compute_daily_returns():
#     engine = get_db_engine()
#
#     query = text("""
#         DROP TABLE IF EXISTS analytics_daily_returns;
#
#         CREATE TABLE analytics_daily_returns AS
#         SELECT
#             date,
#             ticker,
#             close,
#             (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
#             / LAG(close) OVER (PARTITION BY ticker ORDER BY date)
#             AS daily_return
#         FROM raw_prices;
#     """)
#
#     with engine.connect() as conn:
#         conn.execute(query)
#         conn.commit()
#
#
# def compute_annualized_volatility():
#     engine = get_db_engine()
#
#     query = text("""
#         DROP TABLE IF EXISTS analytics_annualized_volatility;
#
#         CREATE TABLE analytics_annualized_volatility AS
#         SELECT
#             ticker,
#             COUNT(*) AS nb_days,
#             AVG(daily_return) * 252 AS annualized_return,
#             STDDEV(daily_return) * SQRT(252) AS annualized_volatility
#         FROM analytics_daily_returns
#         WHERE daily_return IS NOT NULL
#         GROUP BY ticker;
#     """)
#
#     with engine.connect() as conn:
#         conn.execute(query)
#         conn.commit()