import pandas as pd

from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze the sentiment polarity of a text.

    Args:
        text (str): The text to analyze.

    Returns:
        float: Sentiment polarity score.
    """
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def start():
    try:
        df = pd.read_csv('../data/MLB_rumors.csv')
        sentiment_df = pd.DataFrame({'title': df['title'], 'sentiment_score': df['content'].apply(analyze_sentiment)})
        sentiment_df.to_csv('../data/sentiment_analysis.csv', index=False)

        print("Sentiment analysis completed.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty DataFrame: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    start()