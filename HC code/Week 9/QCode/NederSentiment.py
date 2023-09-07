import pandas as pd
import pattern
from pattern.text.nl import sentiment as dutch_sentiment

# Load CSV file into a DataFrame
df = pd.read_csv('..\Week 8\CSV files\Bol_com_reviews_metSterren.csv', on_bad_lines='skip')


# Define a function to get sentiment score for each row in DataFrame
def get_sentiment_score(text):
    return dutch_sentiment(text)[0]


# Apply the function to DataFrame to get sentiment score for each row
df['sentiment_score'] = df['reviews'].apply(get_sentiment_score)

# Classify sentiment as positive, negative or neutral based on sentiment score threshold
df['sentiment'] = df['sentiment_score'].apply(
    lambda score: 'positive' if score > 0 else ('negative' if score < 0 else 'neutral'))

# Save the updated DataFrame to a new CSV file
df.to_csv('file_with_dutch_sentiment.csv', index=False)