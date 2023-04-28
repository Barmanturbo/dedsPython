import pandas as pd
import pyodbc
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Maak verbinding met de Microsoft Access-database
conn_str_sales = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\Week 10\\GO-databases schoon\\go_sales_schoon.accdb;"
    r"ExtendedAnsiSQL=1;"
)
conn_SALES = pyodbc.connect(conn_str_sales)

# Haal gegevens op uit de database
df_returnedItems = pd.read_sql_query("SELECT * FROM returned_item", conn_SALES)
df_details = pd.read_sql_query("SELECT * FROM order_details", conn_SALES)
df_header = pd.read_sql_query('SELECT * FROM order_header', conn_SALES)

#JOIN tabel
df = pd.merge(df_returnedItems, df_details, on='ORDER_DETAIL_CODE')
df = pd.merge(df,df_header, on='ORDER_NUMBER')


# Selecteer de relevante kolommen
df = df[['ORDER_DATE', 'RETURN_QUANTITY']]

# Maak een nieuwe kolom aan met de maand van elke order
df['MONTH'] = pd.to_datetime(df['ORDER_DATE']).dt.month

# Groepeer de gegevens per maand en bereken de som van de geretourneerde hoeveelheden
df_monthly = df.groupby('MONTH').sum().reset_index()

# Scheid de onafhankelijke en afhankelijke variabelen
X = df_monthly[['MONTH']]
y = df_monthly['RETURN_QUANTITY']

# Schaal de gegevens
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Maak een lineair regressiemodel en pas het toe op de geschaalde gegevens
model = LinearRegression()
model.fit(X_scaled, y)
y_pred = model.predict(X_scaled)

# Bereken de r2-score op de ongeschaalde gegevens
r2 = r2_score(y, y_pred)
print(r2)
