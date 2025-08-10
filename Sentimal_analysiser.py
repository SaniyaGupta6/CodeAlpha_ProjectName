import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

user_text = input("Enter the text you want to analyze: ")

def classify_sentiment(text):
    score = sia.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

sentiment = classify_sentiment(user_text)

print(f"\nThe sentiment of the input text is: {sentiment}")