import requests
import csv
import pandas as pd

from bs4 import BeautifulSoup
from collections import Counter
from itertools import combinations
from textblob import TextBlob


def get_data(url):
    """
    Fetch data from a given URL and return it as a BeautifulSoup object.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        BeautifulSoup: The parsed HTML content.

    Raises:
        requests.exceptions.ConnectionError: If a connection error occurs.
    """
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        res.encoding = 'utf-8'
        data = BeautifulSoup(res.text, 'html.parser')

        return data

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")

        return None


def get_user_input():
    """
    Prompt the user to enter desired years and months for data retrieval.

    Returns:
        tuple: Lists of selected years and months.
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


def get_article_content(raw_data):
    """
    Extract article content from a BeautifulSoup object.

    Args:
        raw_data (BeautifulSoup): The parsed HTML content.

    Returns:
        tuple: A list of articles and the URL of the last article.
    """
    url_keyword_list = []
    articles_list = []
    all_content = raw_data.select('.content .entry-title a')

    for keyword in all_content:
        url_slice = str(keyword).split('mlbtraderumors.com/')[1].split('"')[0]
        url_keyword_list.append(url_slice)

    for url_slice_keyword in url_keyword_list:
        article_url = f'https://www.mlbtraderumors.com/{url_slice_keyword}'
        articles = get_data(article_url)
        if articles:
            articles_list.append(articles)

    return articles_list, article_url


def data_cleaning(articles, url):
    """
    Clean and format article data.

    Args:
        articles (list): List of BeautifulSoup objects representing articles.
        url (str): The URL of the last article.

    Returns:
        tuple: A list of cleaned article data and the updated article count.
    """
    final_data = []
    for article in articles:
        article_title = article.select('.content .entry-header .entry-title')
        title = str(article_title).split('>')[1].strip('</h1')
        article_content = article.select('.content .entry-content')

        for sentences in article_content:
            final_text = sentences.text.strip('\n')


        article_tags = article.select('.entry-meta .entry-categories')
        tags_mix = str(article_tags).split('>')
        tags_list = []

        for tags in tags_mix:
            if '</a' in tags:
                tag = tags.strip('</a')
                tags_list.append(tag)
                final_tags = ';'.join(tags_list)

        article_date = article.select('.entry-meta .entry-time')
        date = str(article_date).split('datetime="')[1].split('T')[0]

        final_data.append((
                    title,
                    url,
                    final_text,
                    final_tags,
                    date
                ))

        print(f'article "{title}" is added.')
        print("----------------------------------------------------------------------")

    return final_data


def transform_to_dataframe(final_data):
    """
    Transform data to dataframe.

    Args:
        final_data (list): Final raw data

    Returns:
        dataframe: MLB rumors data
    """
    columns = ['title', 'url', 'content', 'tags', 'date']
    df = pd.DataFrame(final_data, columns=columns)

    return df


def tag_analysis(data, bucket_name):

    teams = [
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago Cubs",
    "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers",
    "Houston Astros", "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins",
    "Milwaukee Brewers", "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", "Seattle Mariners",
    "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"
]

    try:
        tags = data['tags'].str.split(';').explode()
        tag_counts = tags.value_counts()
        co_occurrence = Counter()

        for _, row in data.iterrows():
            tags_in_row = row['tags'].split(';')
            filtered_tags_in_row = [tag for tag in tags_in_row if tag in teams or 'transaction' in tag.lower()]
            co_occurrence.update(combinations(filtered_tags_in_row, 2))

        filtered_tags_df = tag_counts[tag_counts.index.isin(teams) | tag_counts.index.str.contains('transaction', case=False)].reset_index()
        filtered_tags_df.columns = ['Tag', 'Count']
        filtered_tags_df.to_csv(f"s3://{bucket_name}/tag_frequencies.csv", index=False)

        common_pairs = co_occurrence.most_common(10)
        co_occurrence_df = pd.DataFrame(common_pairs, columns=['Tag Pair', 'Co-occurrence Count'])
        co_occurrence_df.to_csv(f"s3://{bucket_name}/tag_co_occurrences.csv", index=False)

        print("Tag analysis completed.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except pd.errors.EmptyDataError as e:
        print(f"Empty DataFrame: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")



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


def sentiment_analysis(data, bucket_name):
    try:
        sentiment_df = pd.DataFrame({'title': data['title'], 'sentiment_score': data['content'].apply(analyze_sentiment)})
        sentiment_df.to_csv(f"s3://{bucket_name}/sentiment_analysis.csv")

        print("Sentiment analysis completed.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty DataFrame: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_to_s3_bucket(data, bucket_name):
    """
    Save cleaned article data to an S3 bucket using pandas.

    Args:
        final_data (list): List of cleaned article data.
        bucket_name (str): Name of the S3 bucket to save the file.
    """

    data.to_csv(f"s3://{bucket_name}/MLB_rumors.csv")


# def save_to_csv(final_data):
#     """
#     Save cleaned article data to a CSV file.

#     Args:
#         final_data (list): List of cleaned article data.
#     """
#     filename = 'data/MLB_rumors.csv'
#     existing_data = []
#     try:
#         with open(filename, 'r', newline='', encoding='utf-8-sig') as csv_file:
#             reader = csv.reader(csv_file)
#             existing_data = list(reader)
#     except FileNotFoundError:
#         pass

#     new_data = []
#     existing_urls = {row[1] for row in existing_data[1:]}
#     for row in final_data:
#         if row[1] not in existing_urls:
#             new_data.append(row)

#     with open(filename, 'a', newline='', encoding='utf-8-sig') as csv_file:
#         writer = csv.writer(csv_file)
#         if not existing_data:
#             writer.writerow(['title', 'url', 'content', 'tags', 'date'])
#         for row in new_data:
#             writer.writerow(row)


def start():
    """
    Main function to execute the data retrieval and cleaning process.
    """
    # years, months = get_user_input()
    # article_num = 0
    # for year, month in zip(years, months):
    #     target_url = f"https://www.mlbtraderumors.com/{year}/{month}"
    #     data = get_data(target_url)
    #     articles, article_url = get_article_content(data)
    #     final_data, article_num = data_cleaning(articles, article_url, article_num)
    #     # save_to_csv(final_data)


    all_data = []

    for year in range(2020, 2024):
        last_month = 10 if year == 2023 else 12

        for month in range(1, last_month + 1):
            target_url = f"https://www.mlbtraderumors.com/{str(year)}/{str(month)}"
            data = get_data(target_url)

            if data is None:
                continue

            articles, article_url = get_article_content(data)
            monthly_data = data_cleaning(articles, article_url)
            all_data.extend(monthly_data)

    df = transform_to_dataframe(all_data)

    save_to_s3_bucket(df, "mlb-rumors-analysis-bucket")
    sentiment_analysis(df, "mlb-rumors-analysis-bucket")
    tag_analysis(df, "mlb-rumors-analysis-bucket")
