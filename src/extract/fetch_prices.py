import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

TICKERS = [
    "MC.PA",
    "SAP.DE",
    "ASML.AS",
    "NESN.SW",
    "SHEL.L"
]


###
# This module is responsible for fetching the stock price data for the specified tickers using the yfinance library.
# Input: A list of tickers and a period ("1y" for 1 year).
# Output: A DataFrame containing the companies' stock prices with columns:
###

def fetch_prices(period="1y"):
    logger.info("Starting price extraction")

    data_frames = []

    for ticker in TICKERS:
        logger.info(f"Downloading {ticker}")

        df = yf.download(ticker, period=period)

        if df.empty:
            logger.warning(f"No data for {ticker}")
            continue

        df["ticker"] = ticker
        # Reset index to have date as a column
        df.reset_index(inplace=True)

        df = df[[
            "Date",
            "ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]]

        # Rename columns to match database schema & SQL lowercase naming convention
        df.columns = [
            "date",
            "ticker",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        data_frames.append(df)

    if len(data_frames) == 0:
        return pd.DataFrame()

    return pd.concat(data_frames)