import calendar
import csv
import nltk
import pandas as pd
import requests

from bs4 import BeautifulSoup
from collections import Counter
from itertools import combinations
from nltk.corpus import stopwords
from textblob import TextBlob
from typing import List, Tuple, Optional


MLB_RUMORS_BASE_URL = 'https://www.mlbtraderumors.com'
TEAMS = [
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago Cubs",
    "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers",
    "Houston Astros", "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins",
    "Milwaukee Brewers", "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", "Seattle Mariners",
    "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"
]
BUCKET_NAME = 'mlb-rumors-analysis-bucket'

# ----------------------------------------- Utility Functions -----------------------------------------


def get_user_input():
    """
    Prompt the user to enter desired years and months for data retrieval.
    """
    years = []
    months = []
    while True:
        year = input("Please enter a desired year (e.g., 2022) or type 'done' to finish: ")

        if year.lower() == 'done':
            break

        month = input("Please enter the desired month as a number (e.g., 5 for May) or type 'done' to finish: ")

        if month.lower() == 'done':
            break

        if year.isdigit() and month.isdigit() and 1 <= int(month) <= 12:
            years.append(year)
            months.append(month)
        else:
            print("Invalid input. Please enter a valid year and month.")

    return years, months


def fetch_html_from_url(url: str) -> Optional[BeautifulSoup]:
    """Retrieve and parse HTML content from a given URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL {url}: {e}")
        return None

# ----------------------------------------- Data Collection Functions -----------------------------------------

def extract_article_links(monthly_page: BeautifulSoup) -> List[str]:
    """Extract all article links from a monthly archive page."""
    articles = monthly_page.select('.content .entry-title a')
    return [link.get('href') for link in articles]

def extract_article_details(article_url: str) -> Optional[Tuple[str, str, str, str, str]]:
    """Extract article details from a single article page."""
    article_page = fetch_html_from_url(article_url)
    if not article_page:
        return None

    title = article_page.select_one('.content .entry-header .entry-title').text
    content = article_page.select_one('.content .entry-content').text.strip('\n')
    tags = ';'.join([tag.text for tag in article_page.select('.entry-meta .entry-categories a')])
    date = article_page.select_one('.entry-meta .entry-time')['datetime'].split('T')[0]

    return title, article_url, content, tags, date

# ----------------------------------------- Analysis Functions -----------------------------------------

def perform_tag_analysis(data: pd.DataFrame) -> None:
    """Analyze and export tag frequencies and co-occurrences."""
    tags = data['tags'].str.split(';').explode()
    tag_counts = tags.value_counts()

    filtered_tags_df = tag_counts[
        tag_counts.index.isin(TEAMS)
    ].reset_index()
    filtered_tags_df.columns = ['Tag', 'Count']
    # filtered_tags_df.to_csv(f"s3://{BUCKET_NAME}/tag_frequencies.csv", index=False)
    filtered_tags_df.to_csv("../data/tag_frequencies.csv", index=False)

    co_occurrence = Counter()
    for _, row in data.iterrows():
        tags_in_row = set(row['tags'].split(';'))
        filtered_tags = [tag for tag in tags_in_row if tag in TEAMS]
        co_occurrence.update(combinations(filtered_tags, 2))

    co_occurrence_df = pd.DataFrame({
        'Tag1': [pair[0] for pair in co_occurrence.keys()],
        'Tag2': [pair[1] for pair in co_occurrence.keys()],
        'Co-occurrence Count': list(co_occurrence.values())
    })
    co_occurrence_df = co_occurrence_df.sort_values(by='Co-occurrence Count', ascending=False).head(10)

    # co_occurrence_df.to_csv(f"s3://{BUCKET_NAME}/tag_co_occurrences.csv", index=False)
    co_occurrence_df.to_csv("../data/tag_co_occurrences.csv", index=False)


def perform_sentiment_analysis(data: pd.DataFrame) -> None:
    """Analyze and export sentiment scores for articles."""
    data['sentiment_score'] = data['content'].apply(lambda text: TextBlob(text).sentiment.polarity)
    sentiment_df = pd.DataFrame({
        'article_id': data['article_id'],
        'title': data['title'],
        'sentiment_score': data['sentiment_score']
    })
    # sentiment_df.to_csv(f"s3://{BUCKET_NAME}/sentiment_analysis.csv", index=False)
    sentiment_df.to_csv("../data/sentiment_analysis.csv", index=False)


def top_words_analysis(data: pd.DataFrame, n=10) -> None:
    """Analyze and export the top n words from the content."""
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))

    baseball_keywords = {"era", "whip", "avg", "rbi", "slugging",
                         "obp", "ops", "plate", "appearance",
                         "run", "hit", "double", "triple", "walk"}

    words_data = []
    for idx, row in data.iterrows():
        content_words = set(row['content'].split())
        for word in content_words:
            if word.lower() not in stop_words and word.lower() in baseball_keywords:
                words_data.append({'Word': word, 'article_id': str(row['article_id'])})

    words_df = pd.DataFrame(words_data)
    word_counts = words_df.groupby('Word').size().reset_index(name='Count')
    word_article_ids = words_df.groupby('Word')['article_id'].apply(list).reset_index()

    top_words_df = pd.merge(word_counts, word_article_ids, on='Word')
    top_words_df = top_words_df.nlargest(n, 'Count')
    # top_words_df.to_csv(f"s3://{BUCKET_NAME}/top_{n}_words.csv", index=False)
    top_words_df.to_csv(f"../data/top_{n}_words.csv", index=False)

# ----------------------------------------- Main Execution -----------------------------------------

def main() -> None:
    """Main execution function."""
    all_articles = []
    # years, months = get_user_input()
    # for year, month in zip(years, months):
    for year in range(2023, 2024):
        print(f"------Starting crawling {year} data------")
        last_month = 10 if year == 2023 else 12
        for month in range(1, last_month + 1):
            month_name = calendar.month_name[month]
            print(f"------------ {month_name} ------------")
            monthly_url = f"{MLB_RUMORS_BASE_URL}/{year}/{month}"
            monthly_page = fetch_html_from_url(monthly_url)
            if not monthly_page:
                continue
            article_links = extract_article_links(monthly_page)
            for article_link in article_links:
                details = extract_article_details(article_link)
                if details:
                    all_articles.append(details)
                    print(f'Article "{details[0]}" added.')

    print("------------------Done!------------------")
    print(f"{len(all_articles)} rumors added.")
    df = pd.DataFrame(all_articles, columns=['title', 'url', 'content', 'tags', 'date'])
    df['article_id'] = df.index
    df = df[['article_id', 'title', 'url', 'content', 'tags', 'date']]
    df.to_csv("../data/MLB_rumors.csv", index=False)
    print("-------Starting sentiment analysis-------")
    perform_sentiment_analysis(df)
    print("------------------Done!------------------")
    print("----------Starting tag analysis----------")
    perform_tag_analysis(df)
    print("------------------Done!------------------")
    print("-------Starting Top Words Analysis-------")
    top_words_analysis(df, 10)
    print("------------------Done!------------------")

    # all_articles = []
    # for year in range(2020, 2024):
    #     last_month = 10 if year == 2023 else 12
    #     for month in range(1, last_month + 1):
    #         monthly_url = f"{MLB_RUMORS_BASE_URL}/{year}/{month}"
    #         monthly_page = fetch_html_from_url(monthly_url)
    #         if not monthly_page:
    #             continue
    #         article_links = extract_article_links(monthly_page)
    #         for article_link in article_links:
    #             details = extract_article_details(article_link)
    #             if details:
    #                 all_articles.append(details)
    #                 print(f'Article "{details[0]}" added.')

    # print("------------------Done!------------------")
    # print(f"{len(all_articles)} rumors added.")
    # df = pd.DataFrame(all_articles, columns=['title', 'url', 'content', 'tags', 'date'])
    # df['article_id'] = df.index
    # df = df[['article_id', 'title', 'url', 'content', 'tags', 'date']]
    # df.to_csv(f"s3://{BUCKET_NAME}/MLB_rumors.csv", index=False)
    # print("-------Starting sentiment analysis-------")
    # perform_sentiment_analysis(df)
    # print("------------------Done!------------------")
    # print("----------Starting tag analysis----------")
    # perform_tag_analysis(df)
    # print("------------------Done!------------------")
    # print("-------Starting Top Words Analysis-------")
    # top_words_analysis(df, 10)
    # print("------------------Done!------------------")

if __name__ == '__main__':
    main()
