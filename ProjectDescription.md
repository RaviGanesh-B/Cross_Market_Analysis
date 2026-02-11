# Cross_Market_Analysis

Hey guys this is an cross_market_analysis based project ,process including datacollection from various datasets,
create sql tables to store data and to perform queries with them to analyze that in multiple approaches, 
then using streamlit we are going to visualize and make it perform as web app and gonna visualize our data

#DATAFRAMES CREATION

Our first step of the project is to create dataframes to fetch datas from API.
we use f string method to read datas from API.
After we fetched data using "requests method (it is an python library)" we have to check for missing values.
If we have missing values we have to drop the missing value columns from dataset using "dropna()" function.
dropna() is a pandas function pandas is also python library to visualize datasets as dataframes
In this project pandas plays major role as we use this for various function like , dropna(),DataFrame(),description() etc.
while creating dataframes we use time function to avoid API crashes while reading it eg:timesleep(20) it is also a python function
finally to_datetime() function to transform it into last_updated column .
By following this flow i created four different frames such as Crypto_currencies , Crypto_prices , Oil_prices and Stock_prices


#SQL connection

Then I connected my MYSQL work bench to jupyter by using cursor method.
After connected our database we gonna create tables for each respective dataframes using sql queries.
then we gonna insert data for each datasets respectively and we are using numpy library to change Nan values into None.
And we use pandas to visualize as dataframes

#SQL querries

We using sql to write 30 different queries .
we just do various analysis using sql queries to analyze data.
such as Crypto_insights,price trend analysis, oil_price analysis , stock platform analysis and cross platform analysis using Join queries

#Streamlit APP

After fully structuring our backend now we using streamlit to visualize our datasets into a web app
Stream lit is a python library  used to make ui app,s
In our app we have 3 respective pages each do 3 different functions such as Market overview , SQL querry runner , Top 5 cryoto analysis

🛠️ Tech Stack Used

*Python (Pandas, Requests, yFinance)
*SQL Database (MySQL / PostgreSQL / SQLite)
*CoinGecko API
*Yahoo Finance API
*Streamlit Dashboard
*Data Cleaning + ETL Pipelines

🌟 Key Learnings

Real-time API data extraction
Building relational financial datasets
SQL analytics + join-based market comparison
End-to-end dashboard deployment using Streamlit
Cross-asset trend exploration

📌 Future Enhancements

Add correlation heatmaps & predictive modeling
Deploy dashboard on Streamlit Cloud
Automate daily ETL updates using scheduling





