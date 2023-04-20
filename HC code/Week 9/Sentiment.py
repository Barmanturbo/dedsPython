from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import re

#https://365datascience.com/tutorials/python-tutorials/Review-analysis-with-python/

dfReviews = pd.read_csv('HC code\Week 8\CSV files\Bol_com_reviews_metSterren.csv')

df = dfReviews.loc[:,['inhoud','Review']]
print(df.head())

print('Amount of rows:' + len(df.index))

def create_sentiment(Review):
    if Review=="['1']" or Review=="['2']":
        return -1
    elif Review=="['4']" or Review=="['5']":
        return 1
    else:
        return 0

df['sentiment'] = df['Review'].apply(create_sentiment)


def clean_data(review):
    no_punc = re.sub(r'[^\w\s]', '', review)
    no_digits = ''.join([i for i in no_punc if not i.isdigit()])
    return(no_digits)

print(df['Review'][0])
df['Review'] = df['Review'.apply(clean_data)]
print(df.head())
print(df['Review'][0])

#Term Frequency -> inverse document frequency
tfidf = TfidfVectorizer(
            strip_accents=None,
            lowercase=False,
            preprocessor=None)
X = tfidf.fit_transform(df['Review'])

#Step 5: Building and Evaluating the Machine Learning Model
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X,y)

lr = LogisticRegression(solver='liblinear')
lr.fit(X_train, y_train)#fit model
preds = lr.predict(X_test) #make predictions

#evaluate the performance
accuracy_score(preds, y_test)
