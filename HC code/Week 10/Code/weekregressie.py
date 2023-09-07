from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd
import pyodbc

# Maak verbinding met de Microsoft Access-database
conn_str_sales = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\Week 10\\GO-databases schoon\\go_sales_schoon.accdb;"
    r"ExtendedAnsiSQL=1;"
)

conn_SALES = pyodbc.connect(conn_str_sales)

SALESdf = pyodbc.connect(conn_str_sales)

df_returnedItems = pd.read_sql_query("SELECT * FROM returned_item", conn_SALES)
df_details = pd.read_sql_query("SELECT * FROM order_details", conn_SALES)
df_header = pd.read_sql_query('SELECT * FROM order_header', conn_SALES)

#JOIN tabel
df = pd.merge(df_returnedItems, df_details, on='ORDER_DETAIL_CODE')
df = pd.merge(df,df_header, on='ORDER_NUMBER')

#Selecteer alleen de relevante informatie
df = df.dropna()
df = df[['ORDER_DATE','RETURN_QUANTITY']]

df['DAY_OF_WEEK'] = pd.to_datetime(df['ORDER_DATE']).dt.dayofweek
df = df.drop(['ORDER_DATE'], axis=1)
X = df[['DAY_OF_WEEK']]
y = df['RETURN_QUANTITY']

model = LinearRegression()
model.fit(X, y)
predicted_returns = model.predict([[1]])
print('Predicted returns: ', predicted_returns)

y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
print('r2: ', r2)

