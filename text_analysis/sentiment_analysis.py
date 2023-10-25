import pandas as pd

from textblob import TextBlob


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def start():
    df = pd.read_csv('../data/MLB_rumors.csv')
    sentiment_df = pd.DataFrame({'title': df['title'], 'sentiment_score': df['content'].apply(analyze_sentiment)})
    sentiment_df.to_csv('../data/sentiment_analysis.csv', index=False)


if __name__ == "__main__":
    start()