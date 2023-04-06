import pandas as pd

import re

df = pd.read_csv("HC code/Week 8/CSV files/Scoutscraper.csv")

woordenlijst = {}

#Trek alle review bodies uit de csv en stop ze in een array
for review in df['ReviewText']:
    for woord in review.split():
        woord = re.sub(r'[\*\(\)\-\.,]','',woord)
        woord = woord.upper()
        if woord in woordenlijst:
            woordenlijst[woord] += 1
        else:
            woordenlijst[woord]=1

word_count_df = pd.DataFrame.from_dict(woordenlijst, orient='index', columns=['Count']).sort_values(by='Count', ascending=False)
word_count_df.to_csv('word_count.csv')

