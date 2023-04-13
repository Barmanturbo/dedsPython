import pandas as pd
import numpy as np
import re

#https://365datascience.com/tutorials/python-tutorials/sentiment-analysis-with-python/

df = pd.read_csv('HC code\Week 8\CSV files\Bol_com_reviews.csv')

dfReview = df.loc[:,['review']]
dfReview.head()

print('Amount of rows:' + len(df.index))

def create_sentiment(rating):
    if rating==1 or rating==2:
        return -1
    elif rating==4 or rating==5:
        return 1
    else:
        return 0
    

def clean_data(review):
    no_punc = re.sub(r'[^\w\s]', '', review)
    no_digits = ''.join([i for i in no_punc if not i.isdigit()])
    return(no_digits)