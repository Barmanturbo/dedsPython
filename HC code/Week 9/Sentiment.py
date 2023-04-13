import pandas as pd

df = pd.read_csv('HC code\Week 8\CSV files\Bol_com_reviews.csv')

dfReview = df.loc[:,['review']]
dfReview.head();