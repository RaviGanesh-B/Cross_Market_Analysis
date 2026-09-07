import streamlit as st
import pandas as pd
import pymysql
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title ="Cross platform analysis",layout = "wide",page_icon = "📊" )


st.title("CROSS PLATFORM ANALYSIS")
st.text("Crypto * Oil * Stock Market | SQL Powered Analysis")

def getconnection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="goku",
        database="cross_platform_analysis"
    )

st.sidebar.header("💻 Analysis Navigation")
page = st.sidebar.radio(
          label ="Select page",
          options = ["📊Market Overview","🔍SQL Querry Runner","🪙Top 5 Crypto Analysis"],
          index = 0,
     )

if page == "📊Market Overview":

    st.header("📊Cross Market Overview")

    conn = getconnection()
    cpa_cursor = conn.cursor()

    cpa_cursor.execute("SELECT DATABASE();")
    st.write("Connected to:", cpa_cursor.fetchone()[0])

    cpa_cursor.execute("SELECT COUNT(*) FROM crypto_prices;")
    st.write("Row Count:", cpa_cursor.fetchone()[0])

    cpa_cursor.execute("SELECT MIN(date), MAX(date) FROM crypto_prices")
    min_date, max_date = cpa_cursor.fetchone()


    start_date = st.date_input("Start Date", value = min_date, min_value = min_date, max_value = max_date)
    end_date = st.date_input("End Date", value = max_date, min_value = min_date, max_value = max_date)

    if st.button("Daily Market Snapshot"):

        query = """
                   SELECT *
                   FROM crypto_prices
                   WHERE date BETWEEN
                   %s AND %s
                   ORDER BY date
                   ASC
                """
        cpa_cursor.execute(query, (start_date, end_date))
        Market_overview_data = cpa_cursor.fetchall()

        Market_overview_df = pd.DataFrame(Market_overview_data, columns = [col[0] for col in cpa_cursor.description])

        if Market_overview_df.empty:
            st.warning("no data found")
        else:
            st.dataframe(Market_overview_df)

if page == "🔍SQL Querry Runner":

    st.header("🔍SQL Querry Runner")
    st.write("⚡ Select a query from the dropdown and click **Run Query** to see results.")

    conn = getconnection()
    cpa_cursor = conn.cursor()

    predefined_queries = {
        "top 3 cryptocurrencies by market cap":"""SELECT id,symbol,name,current_price,
                                                  total_volume,circulating_supply,
                                                  total_supply,
                                                  ath,atl,last_updated
                                                  FROM crypto_currencies ORDER BY market_cap DESC LIMIT 3;""",
        "circulating supply exceeds 90% of total supply":"""SELECT id,symbol,name,current_price,
                                                            (circulating_supply/total_supply) * 100 AS supply_percent
                                                             FROM crypto_currencies
                                                             WHERE total_supply IS NOT NULL
                                                             AND circulating_supply / total_supply > 0.9
                                                             ORDER BY supply_percent DESC ;""",
        "10% of their all-time-high (ATH)":"""SELECT id,symbol,name,current_price,ath,
                                             (current_price/ath) * 100 AS ath_percent
                                             FROM crypto_currencies
                                             WHERE ath IS NOT NULL
                                             AND current_price/ath >= 0.9
                                             ORDER BY ath_percent DESC ;""",
        " average market cap rank of coins with volume above $1B.":"""SELECT AVG(market_rank) AS avg_market_cap_rank
                                                                      FROM crypto_currencies
                                                                      WHERE total_volume > 1000000000;""",
        "most recently updated coin":"""SELECT * FROM crypto_currencies
                                        AS most_recentlty_updated_coin
                                        ORDER BY last_updated DESC
                                        LIMIT 1;""",
        " highest daily price of Bitcoin in the last 365 days":"""SELECT MAX(price_usd) AS highest_daily_price FROM
                                                                  crypto_prices
                                                                  WHERE coin_id = "bitcoin"
                                                                  AND date >= CURRENT_DATE - INTERVAL 365 DAY;""",
        " average daily price of Ethereum in the past 1 year":"""SELECT AVG(price_usd) AS avg_dailyprice_ethereum 
                                                                 FROM crypto_prices
                                                                 WHERE coin_id = "ethereum"
                                                                 AND date >= CURRENT_DATE - INTERVAL 365 DAY;""",
        "daily price trend of Bitcoin in March 2025":"""SELECT date,price_usd 
                                                          FROM crypto_prices
                                                          WHERE coin_id = "bitcoin"
                                                          AND date BETWEEN "2025-03-01" AND "2025-03-31"
                                                          ORDER BY date ASC""",
        " coin with the highest average price over 1 year":"""SELECT coin_id, AVG(price_usd)
                                                              AS highest_average_yearly
                                                              FROM crypto_prices
                                                              WHERE date >= CURRENT_DATE - INTERVAL 365 DAY
                                                              GROUP BY coin_id
                                                              ORDER BY highest_average_yearly
                                                              DESC LIMIT 1;""",
        "Get the % change in Bitcoin’s price between feb 2025 to feb 2026 completed":"""SELECT ((feb2026.price_usd - feb2025.price_usd)/ feb2026.price_usd)
                                                                                        * 100 AS bitcoin_percent_change
                                                                                        FROM
                                                                                        (SELECT price_usd FROM crypto_prices
                                                                                        WHERE coin_id = "bitcoin" AND
                                                                                       date BETWEEN "2025-02-01" AND "2025-02-28"
                                                                                       ORDER BY date DESC
                                                                                      LIMIT 1
                                                                                       ) AS feb2025,

                                                                                       (SELECT price_usd FROM crypto_prices
                                                                                       WHERE coin_id = "bitcoin" AND
                                                                                      date BETWEEN "2026-02-01" AND "2026-02-28"
                                                                                       ORDER BY date DESC
                                                                                      LIMIT 1) AS feb2026;
                                                                                      """,
        "highest oil price in the last 5 years":"""SELECT MAX(price_usd) AS 
                                                highest_oil_price_of_5years 
                                                FROM oil_prices
                                                WHERE date >= CURRENT_DATE - INTERVAL 5 YEAR
                                                ORDER BY price_usd DESC
                                                LIMIT 1;""",
        "average oil price per year":"""SELECT 
                                        YEAR(date) AS year,
                                        AVG(price_usd) AS average_oil_price_per_year
                                        FROM oil_prices
                                        GROUP BY YEAR(date)
                                        ORDER BY year;""",
        " oil prices during COVID crash (March–April 2020)":"""SELECT date,price_usd FROM oil_prices
                                                               WHERE date BETWEEN "2020-03-01" AND "2020-04-30"
                                                               ORDER BY date ASC""",
        "lowest price of oil in the last 10 years":"""SELECT date, price_usd AS 
                                                    lowest_oil_price_of_10years 
                                                    FROM oil_prices
                                                    WHERE date >= CURRENT_DATE - INTERVAL 10 YEAR
                                                    ORDER BY price_usd ASC
                                                    LIMIT 1;
                                                    """,
        "volatility of oil prices":"""SELECT 
                                      YEAR(date) AS year,
                                      MAX(price_usd) AS Maxprice,
                                      MIN(price_usd) AS Minprice,
                                     (MAX(price_usd) - MIN(price_usd)) AS votality_of_oil_prices
                                     FROM oil_prices
                                     GROUP BY YEAR(date)
                                     ORDER BY year;
                                    """,
        "all stock prices for a given ticker":"""SELECT * FROM stock_prices
                                              WHERE ticker IN  ("^GSPC","^IXIC","^NSEI")
                                              ORDER BY ticker,date ASC""",
        "highest closing price for NASDAQ (^IXIC)":"""SELECT date,close FROM stock_prices
                                                   WHERE ticker = "^IXIC" ORDER BY 
                                                   close DESC LIMIT 1;""",
        "top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":"""SELECT date,high,low,
                                                                                     (high - low) AS top_5_price_differance_gspc
                                                                                      FROM stock_prices
                                                                                      WHERE ticker = "^GSPC"
                                                                                      ORDER BY  top_5_price_differance_gspc
                                                                                      DESC LIMIT 5;""",
        "monthly average closing price for each ticker":"""SELECT ticker,
                                                           DATE_FORMAT(date, "%Y-%m") AS month,
                                                           AVG(close) AS monthly_average_closing_price
                                                           FROM stock_prices
                                                           GROUP BY ticker, month
                                                           ORDER BY ticker, month
                                                          """,
        "average trading volume of NSEI in 2024":"""SELECT ticker,
                                                  AVG(volume) AS average_trading_volume_2024
                                                  FROM stock_prices
                                                  WHERE ticker = "^NSEI"
                                                  AND YEAR(date) = 2024;
                                                 """,
        " Bitcoin vs Oil average price in 2025":"""SELECT 
                                                   bitcoin.avg_bitcoin_price_2025,
                                                   oil.avg_oil_price_2025
                                                   FROM
                                                   (SELECT AVG(price_usd) AS avg_bitcoin_price_2025
                                                   FROM crypto_prices
                                                   WHERE coin_id = "bitcoin"
                                                   AND YEAR(date) = 2025) AS bitcoin
                    
                                                  JOIN
                    
                                                 (SELECT AVG(price_usd) AS avg_oil_price_2025
                                                 FROM oil_prices
                                                 WHERE YEAR(date) = 2025)
                                                 AS oil
                                                 """,
        "Bitcoin moves with S&P 500":"""SELECT 
                  bitcoin.date,
                  bitcoin.price_usd AS bitcoin_price,
                  sp.close AS sp500_close
                  FROM crypto_prices bitcoin
                  JOIN stock_prices sp
                  ON bitcoin.date = sp.date
                  WHERE bitcoin.coin_id ="bitcoin"
                  AND sp.ticker = "^GSPC"
                  AND YEAR(bitcoin.date) = 2025
                  ORDER BY bitcoin.date;
                  """,
        " Ethereum and NASDAQ daily prices for 2025.":"""SELECT ethereum.date,
                          ethereum.price_usd AS ethereum_price,
                          nasdaq.close AS nasdaq_close
                          FROM crypto_prices ethereum
                          JOIN stock_prices nasdaq
                          ON ethereum.date = nasdaq.date
                          WHERE ethereum.coin_id = 'ethereum'
                          AND nasdaq.ticker = '^IXIC'
                          AND YEAR(ethereum.date) = 2025
                          ORDER BY ethereum.date;
                          """,
        "oil price spiked and compare with Bitcoin price change":"""
                             SELECT *
                             FROM(
                             SELECT oil.date,
                             oil.price_usd AS oil_price,
                             oil.price_usd - LAG(oil.price_usd) OVER (ORDER BY oil.date) AS oil_spike,
                             bitcoin.price_usd AS bitcoin_price,
                             bitcoin.price_usd - LAG(bitcoin.price_usd) OVER (ORDER BY bitcoin.date) AS bitcoin_change
                             FROM oil_prices oil
                             JOIN crypto_prices bitcoin
                             ON oil.date = bitcoin.date
                             WHERE bitcoin.coin_id = 'bitcoin'
                             AND YEAR(oil.date) = 2025 
                             ) AS t
                             WHERE oil_spike > oil_price * 0.05 
                             ORDER BY date;
                             """,
        "top 3 coins daily price trend vs Nifty (^NSEI)":"""SELECT 
                crypto.date,
                crypto.coin_id,
                crypto.price_usd AS coin_price,
                stock.close AS nifty_close
                FROM crypto_prices crypto
                JOIN stock_prices stock
                ON crypto.date = stock.date
                WHERE crypto.coin_id IN ('bitcoin','ethereum','tether')
                AND stock.ticker = "^NSEI"
                AND YEAR(crypto.date) = 2025
                ORDER BY crypto.date, crypto.coin_id;
             """,
        " stock prices (^GSPC) with crude oil prices on the same dates":"""
              SELECT
                  stock.date,
                  stock.close AS sp500_close,
                  oil.price_usd AS oil_price
              FROM stock_prices stock
              JOIN oil_prices oil
                 ON stock.date = oil.date
              WHERE stock.ticker = '^GSPC'
                AND YEAR(stock.date) = 2025
              ORDER BY stock.date;
              """,
        "Bitcoin closing price with crude oil closing price":"""SELECT 
                    bitcoin.date,
                    bitcoin.price_usd AS bitcoin_price,
                    oil.price_usd AS oil_price
                    FROM crypto_prices bitcoin
                    JOIN oil_prices oil
                    ON bitcoin.date = oil.date
                    WHERE bitcoin.coin_id = 'bitcoin'
                    AND YEAR(bitcoin.date) = 2025
                    ORDER BY bitcoin.date;
                    """,
        "NASDAQ (^IXIC) with Ethereum price trends":"""
                     SELECT ethereum.date,
                     ethereum.price_usd AS ethereum_price,
                     nasdaq.close AS nasdaq_close
                     FROM crypto_prices ethereum
                     JOIN stock_prices nasdaq
                     ON ethereum.date = nasdaq.date
                     WHERE ethereum.coin_id = 'ethereum'
                     AND nasdaq.ticker = '^IXIC'
                     AND YEAR(ethereum.date) = 2025
                     ORDER BY ethereum.date;
                     """,
        " top 3 crypto coins with stock indices for 2025":"""
                                 SELECT 
                                 crypto.date,
                                 crypto.coin_id,
                                 crypto.price_usd AS coin_price,
                                 nsei.close AS nifty_close,
                                 gspc.close AS sp500_close,
                                 ixic.close AS nasdaq_close
                                 FROM crypto_prices crypto
                                 JOIN stock_prices nsei
                                 ON crypto.date = nsei.date AND nsei.ticker = '^NSEI'
                                 JOIN stock_prices gspc
                                 ON crypto.date = gspc.date AND gspc.ticker = '^GSPC'
                                 JOIN stock_prices ixic
                                 ON crypto.date = ixic.date AND ixic.ticker = '^IXIC'
                                 WHERE crypto.coin_id IN ('bitcoin','ethereum','tether')
                                 AND YEAR(crypto.date) = 2025
                                 ORDER BY crypto.date, crypto.coin_id;
                                 """,
        "stock prices, oil prices, and Bitcoin prices for daily comparison":"""
                    SELECT bitcoin.date,
                           bitcoin.price_usd AS bitcoin_price,
                           oil.price_usd AS oil_price,
                           nsei.close AS nifty_close,
                           gspc.close AS sp500_close,
                           ixic.close AS nasdaq_close
                    FROM crypto_prices bitcoin
                    JOIN oil_prices oil
                        ON bitcoin.date = oil.date
                    JOIN stock_prices nsei
                        ON bitcoin.date = nsei.date AND nsei.ticker = '^NSEI'
                    JOIN stock_prices gspc
                        ON bitcoin.date = gspc.date AND gspc.ticker = '^GSPC'
                    JOIN stock_prices ixic
                        ON bitcoin.date = ixic.date AND ixic.ticker = '^IXIC'
                    WHERE bitcoin.coin_id = 'bitcoin'
                      AND YEAR(bitcoin.date) = 2025
                    ORDER BY bitcoin.date;
                    """
            
    }

    selected_query_name = st.selectbox(
        "Choose SQL Query",
        options=list(predefined_queries.keys())
    )

    if st.button("Run Query"):
        query = predefined_queries[selected_query_name]
        try:
            cpa_cursor.execute(query)
            Sql_query_data = cpa_cursor.fetchall()

            if cpa_cursor.description:
                Sql_query_df = pd.DataFrame(Sql_query_data,columns = [col[0] for col in cpa_cursor.description])
                st.dataframe(Sql_query_df,use_container_width = True)
            else:
                st.write(Sql_query_data)
        except Exception as e:
            st.error(f"Error Running Query : {e}")


if page == "🪙Top 5 Crypto Analysis":

    st.header("🪙Top 5 Crypto Analysis")

    st.write("Select a cryptocurrency and a date range to view daily prices and trends.")

    conn = getconnection()
    cpa_cursor = conn.cursor()

    cpa_cursor.execute("""SELECT id, name FROM crypto_currencies ORDER BY market_cap DESC LIMIT 5;""")
    Crypto_analysis_data = cpa_cursor.fetchall()

    coin_dict = {coin[0] : coin[1] for coin in Crypto_analysis_data}

    selected_coin_id = st.selectbox(
        "Select Cryptocurrency",
        options = list(coin_dict.keys()),
        format_func=lambda x: coin_dict[x]
    )
    
    cpa_cursor.execute(
        "SELECT MIN(date), MAX(date) FROM crypto_prices WHERE coin_id = %s",
        (selected_coin_id,)
    )
    min_date, max_date = cpa_cursor.fetchone()

    start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

    if st.button("show daily prices"):
        cpa_cursor.execute("""
            SELECT date, price_usd
            FROM crypto_prices
            WHERE coin_id = %s AND date BETWEEN %s AND %s
            ORDER BY date ASC
            """, (selected_coin_id, start_date, end_date))
        daily_data = cpa_cursor.fetchall()
        
        if not daily_data:
            st.warning("no data found")
        else:
            daily_df = pd.DataFrame(daily_data , columns = [col[0] for col in cpa_cursor.description])

            st.dataframe(daily_df, use_container_width=True)

            plt.figure(figsize=(12,6))
            plt.style.use('dark_background')
            sns.lineplot(x='date', y='price_usd', data=daily_df, palette='viridis')

            plt.xticks(rotation=45)
            plt.title(f"{coin_dict[selected_coin_id]} Daily Prices")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.tight_layout()

            st.pyplot(plt)
