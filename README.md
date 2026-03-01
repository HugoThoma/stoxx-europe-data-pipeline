# STOXX Europe 600 - Company Health Data Pipleine

This project implements an end-to-end  data pipelin that :

- Extracts financiel market and fundamental data;
- Store raw historical data in PostgreSQL;
- Transform daa into analytical models;
- Computes a multi-facto company health score;
- Exposes structured dataset fo BI or API usage.

## *Subject might change in time*

### Data Architecture
1. Raw layer : ingestion from Yahoo Finance
2. Transform layer : SQL-based modeling
3. Mart layer : healh scoring model

### Tech Stack
- Python
- PostgreSQL
- SQL
- yfinance
- pandas
- SQLAlchemy




## *How To*

### Run the project 

1. Create or open venv :

```Bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
*-To open only-*
```Bash
venv\Scripts\activate
```

2. Configure envionment variables in .env
3. Creat PostgreSQL database
4. Run pipeline :
```Bash
python main.py
```
