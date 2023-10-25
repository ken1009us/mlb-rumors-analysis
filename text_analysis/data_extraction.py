import requests
import csv


from bs4 import BeautifulSoup


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


def data_cleaning(articles, url, article_num):
    """
    Clean and format article data.

    Args:
        articles (list): List of BeautifulSoup objects representing articles.
        url (str): The URL of the last article.
        article_num (int): The number of articles processed.

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
        article_num += 1

        print(f'article "{title}" is added.')
        print("----------------------------------------------------------------------")

    return final_data, article_num


def save_to_csv(final_data):
    """
    Save cleaned article data to a CSV file.

    Args:
        final_data (list): List of cleaned article data.
    """
    filename = 'data/MLB_rumors.csv'
    existing_data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)
            existing_data = list(reader)
    except FileNotFoundError:
        pass

    new_data = []
    existing_urls = {row[1] for row in existing_data[1:]}
    for row in final_data:
        if row[1] not in existing_urls:
            new_data.append(row)

    with open(filename, 'a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        if not existing_data:
            writer.writerow(['title', 'url', 'content', 'tags', 'date'])
        for row in new_data:
            writer.writerow(row)


def start():
    """
    Main function to execute the data retrieval and cleaning process.
    """
    years, months = get_user_input()
    article_num = 0
    for year, month in zip(years, months):
        target_url = f"https://www.mlbtraderumors.com/{year}/{month}"
        data = get_data(target_url)
        articles, article_url = get_article_content(data)
        final_data, article_num = data_cleaning(articles, article_url, article_num)
        save_to_csv(final_data)

    print("articles be added:", article_num)


if __name__ == "__main__":
    start()