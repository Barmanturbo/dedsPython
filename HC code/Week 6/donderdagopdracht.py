import pandas as pd
import pyodbc

# Maak verbinding met de Microsoft Access-database
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\databases\\go_sales.accdb;"
    r"ExtendedAnsiSQL=1;"
)
conn = pyodbc.connect(conn_str)

# Haal de gegevens op uit de order_details en order_header tabellen
df_details = pd.read_sql_query("SELECT * FROM order_details", conn)
df_header = pd.read_sql_query("SELECT * FROM order_header", conn)
df_product = pd.read_sql_query("SELECT * FROM product", conn)

df_METHOD = pd.read_sql_query("SELECT ORDER_METHOD_CODE FROM order_header", conn)
df_TIJD = pd.read_sql_query("SELECT ORDER_DATE FROM order_header", conn)


# Voer de join uit en selecteer de gewenste kolommen
dfBesteldProduct = pd.merge(df_details, df_header, on='ORDER_NUMBER')
dfBesteldProduct = dfBesteldProduct[['ORDER_DETAIL_CODE', 'ORDER_DATE', 'ORDER_METHOD_CODE', 'PRODUCT_NUMBER', 'UNIT_SALE_PRICE']]

dfPRODUCT = pd.merge(df_product,df_details, on='PRODUCT_NUMBER')
dfPRODUCT = dfPRODUCT[['PRODUCT_NUMBER','PRODUCT_NAME','DESCRIPTION','UNIT_SALE_PRICE']]

    #Ja het is redundant maar toch schrijf ik het voor de zekerheid op voor de consistentie en volledigheid
dfBESTELLING = pd.merge(df_details, df_header, on='ORDER_NUMBER')

df_DATE = pd.DataFrame({'ORDER_DATE': df_TIJD['ORDER_DATE'], 'YEAR': pd.DatetimeIndex(df_TIJD['ORDER_DATE']).year})


# Print het resultaat dataframe
print(dfBesteldProduct)
print(dfPRODUCT)
print(dfBESTELLING)

print(df_METHOD)
print(df_DATE)

# Output naar csv bestand
dfBesteldProduct.to_csv('donderdagpythonopdracht.csv', index=False)
dfPRODUCT.to_csv('dimPRODUCT.csv', index=False)
dfBESTELLING.to_csv('dimBESTELLING.csv', index=False)

df_METHOD.to_csv('dimMETHOD.csv', index=False)

df_DATE.to_csv('dimDATE.csv', index=False)
