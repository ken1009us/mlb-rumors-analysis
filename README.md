# MLB Rumors Analysis

This project includes a comprehensive data pipeline for collecting, processing, and analyzing MLB rumors. It derives important insights from complex data streams by combining the power of sophisticated analytics with the scalability of AWS services (S3, EC2) and the automation capabilities of Airflow. It generates significant insights from raw data and easily presents them in Tableau through intuitive visualizations, providing a comprehensive perspective of the MLB rumors landscape.

## Pipeline Flow Chart

<a href="url"><img src="https://github.com/ken1009us/mlb-rumors-analysis/blob/main/img/pipeline.png"></a>

## Technology Integration

- Python
- TextBlob for Sentiment Analysis
- pandas for Data Manipulation
- Apache Airflow for Orchestrating Data Pipeline
- Amazon EC2 for Deployment
- Amazon S3 for Data Storage
- Tableau for Data Visualization

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11.5
- TextBlob library
- pandas library
- Apache Airflow installed and configured
- Amazon AWS account with EC2 and S3 access
- Tableau Desktop or Tableau Public

## Installation

Install the required Python libraries:

```bash
$ pip install textblob pandas
```

Clone this repository to your local machine:

```bash
$ git clone https://github.com/ken1009us/mlb-rumors-analysis.git
```

## Usage

1. Configure Apache Airflow and define a DAG to orchestrate the data pipeline for MLB rumors data extraction, transformation, and loading (ETL).
2. Run the Airflow DAG to automatically handle data extraction, perform sentiment analysis on MLB rumors data, and load the processed data.
3. Load the generated CSV files into Amazon S3.
4. Configure Tableau to connect to the S3 bucket and visualize the data.

## Files

- MLB_rumors.csv: Raw MLB rumors data.
- tag_frequencies.csv: Tag frequencies for team names and "transaction."
- tag_co_occurrences.csv: Co-occurrence of tags.
- sentiment_analysis.csv: Sentiment scores for MLB rumors articles.

## Result

### Tag Analysis Report:

1. Tag Frequencies:

- A list of tags (which are MLB teams and the term "transaction") and their respective counts. This report would tell you how often each team (or transaction) is mentioned in the articles.

- For visualization in Tableau:
  - A bar chart where each bar represents a team or transaction, and the height of the bar corresponds to the frequency of that tag.

2. Tag Co-occurrences:

- A list of pairs of tags and how often they appear together in the same article. This helps in identifying which teams or transactions are frequently mentioned together, possibly indicating interactions or comparisons between them.

- For visualization in Tableau:
  - A heatmap where each cell corresponds to a pair of tags, and the color intensity indicates the frequency of their co-occurrence. Darker cells would indicate pairs of tags that often appear together.

### Sentiment Analysis Report:

1. Sentiment Scores:

- For each article, a sentiment score is calculated. This score, which ranges from -1 to 1, indicates the overall sentiment of the article. Negative values suggest negative sentiment, positive values suggest positive sentiment, and values close to zero indicate neutral sentiment.

- For visualization in Tableau:
  - A histogram showing the distribution of sentiment scores, allowing you to quickly see the general sentiment trend across articles.
  - A scatter plot with articles on the y-axis and their corresponding sentiment scores on the x-axis. This visualization will let you pinpoint specific articles with strong positive or negative sentiment.

2. Overall Sentiment Trend:

- While not explicitly mentioned in the code, a subsequent analysis could involve plotting the average sentiment scores over time (e.g., monthly or yearly). This would help in understanding how sentiments towards MLB teams and transactions have evolved.
- For visualization in Tableau:
  - A line chart where the x-axis represents time (month/year) and the y-axis represents the average sentiment score. Peaks would indicate times of positive sentiment, while troughs indicate negative sentiment periods.

## Project Origin

This project was inspired by the need to gain insights from MLB rumors data and visualize sentiment trends.

## Disclaimer

The information provided in this project is for educational and analytical purposes only. It does not constitute financial, legal, or professional advice.