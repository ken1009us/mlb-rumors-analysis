# MLB Rumors Analysis

This project analyzes MLB rumors data, performs analysis, and visualizes the results using Tableau.

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

## Project Origin

This project was inspired by the need to gain insights from MLB rumors data and visualize sentiment trends.

## Disclaimer

The information provided in this project is for educational and analytical purposes only. It does not constitute financial, legal, or professional advice.