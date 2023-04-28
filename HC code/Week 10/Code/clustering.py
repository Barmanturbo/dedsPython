import pandas as pd
import pyodbc
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Maak verbinding met de eerste database
con_sales = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\Week 10\\GO-databases schoon\\go_sales_schoon.accdb;')

# Lees de gegevens uit de eerste tabel
sales_data = pd.read_sql("SELECT * FROM order_details JOIN returned_item ON order_details.ORDER_DETAIL_CODE = returned_item.ORDER_DETAIL_CODE JOIN product ON order_details.PRODUCT_NUMBER = product.PRODUCT_NUMBER JOIN order_header ON order_details.ORDER_NUMBER = order_header.ORDER_NUMBER JOIN sales_sales_branch ON order_header.RETAILER_SITE_CODE = sales_sales_branch.ADRESS1 JOIN sales_retailer_site ON order_header.RETAILER_SITE_CODE = sales_retailer_site.RETAILER_SITE_CODE", con_sales)

# Maak verbinding met de tweede database
con_crm = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\Week 10\\GO-databases schoon\\crm.accdb;')

# Lees de gegevens uit de tweede tabel
crm_data = pd.read_sql("SELECT * FROM retailer", con_crm)

# Voeg de twee tabellen samen op basis van de RETAILER_CODE
merged_data = pd.merge(sales_data, crm_data, on="RETAILER_CODE")

# Selecteer de relevante kenmerken voor de clustering
selected_features = ["QUANTITY", "UNIT_COST", "UNIT_PRICE", "UNIT_SALE_PRICE", "COMPANY_NAME", "RETAILER_TYPE_CODE"]

# Maak een subset van de data met alleen de geselecteerde kenmerken
cluster_data = merged_data[selected_features]

# Standaardiseer de gegevens
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data)

# Bepaal het aantal clusters met behulp van de elbow-methode
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=0)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)
    
# Plot de elbow curve
import matplotlib.pyplot as plt
plt.plot(range(1, 11), wcss)
plt.title('Elbow Curve')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Selecteer het optimale aantal clusters
n_clusters = 4

# Pas het KMeans-clusteringalgoritme toe op de gestandaardiseerde gegevens
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=0)
kmeans.fit(scaled_data)

# Voeg de clusterlabels toe aan de gegevens
cluster_data["Cluster"] = kmeans.labels_

# Controleer de overeenkomst met de kolom RETAILER_TYPE_CODE
cross_tab = pd.crosstab(cluster_data["Cluster"], cluster_data["RETAILER_TYPE_CODE"])
print(cross_tab)
