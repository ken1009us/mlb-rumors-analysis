# MLB Rumors Analysis

This project includes a comprehensive data pipeline for collecting, processing, and analyzing MLB rumors. It derives important insights from complex data streams by combining the power of sophisticated analytics with the scalability of AWS services (S3, EC2) and the automation capabilities of Airflow. It generates significant insights from raw data and easily presents them in Tableau through intuitive visualizations, providing a comprehensive perspective of the MLB rumors landscape.

## Pipeline Flow Chart

![image](https://github.com/ken1009us/mlb-rumors-analysis/blob/master/img/pipeline-flow-chart.png "pipeline")

## Tableau Dashboard

![image](https://github.com/ken1009us/mlb-rumors-analysis/blob/master/img/dashboard.png "dashboard")

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

1. Execute the script to start collecting data from the "MLB Trade Rumors" website for the specified years and months.
2. The script will save the data in CSV files: MLB_rumors.csv, tag_frequencies.csv, tag_co_occurrences.csv, 3. sentiment_analysis.csv, and top_words_analysis.csv.
4. Use any data visualization tool like Tableau to visualize the generated data.

## Files

- MLB_rumors.csv: Raw MLB rumors data.
- tag_frequencies.csv: Tag frequencies for team names.
- tag_co_occurrences.csv: Co-occurrence of team tags.
- sentiment_analysis.csv: Sentiment scores for MLB rumors articles.
- top_words_analysis.csv: Top N words used in the articles.

## Result

### Tag Analysis Report:

1. Tag Frequencies:

- A list of tags, which predominantly consist of MLB teams and the term "transactions," showcasing their respective mention counts in the articles. From the dashboard, teams like the Minnesota Twins, Cincinnati Reds, and San Francisco Giants were frequently discussed.

2. Tag Co-occurrences:

- A list showing pairs of tags and their joint appearance frequency in the same article. From the dashboard, it's evident that the Milwaukee Brewers and Chicago Cubs co-occur most frequently, indicating potential interactions or discussions between them.

### Sentiment Analysis Report:

1. Sentiment Scores:

- Each article possesses a sentiment score, ranging from negative values, suggesting negative sentiment, to positive values indicating positive sentiment. From the dashboard, articles tagged with Houston Astros recorded the highest positive sentiment score.

2. Overall Sentiment Trend:

- While not explicitly mentioned in the code, a subsequent analysis could involve plotting the average sentiment scores over time (e.g., monthly or yearly). This would help in understanding how sentiments towards MLB teams and transactions have evolved.

### Top Baseball Keywords Analysis:

- This report showcases the most frequently mentioned baseball keywords in the articles, exempting common stop words. From the dashboard, predominant words like hit, ERA, and walk were prevalent. Their respective counts are listed.

## Project Origin

This project was inspired by the need to gain insights from MLB rumors data and visualize sentiment trends.

## Disclaimer

The information provided in this project is for educational and analytical purposes only. It does not constitute financial, legal, or professional advice.

## Author

- Name: Ken Wu
- Email: shwu2@illinois.edu
