import pandas as pd

from collections import Counter
from itertools import combinations


teams = [
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago Cubs",
    "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers",
    "Houston Astros", "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins",
    "Milwaukee Brewers", "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", "Seattle Mariners",
    "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"
]


def start():
    try:
        df = pd.read_csv('../data/MLB_rumors.csv')
        tags = df['tags'].str.split(';').explode()
        tag_counts = tags.value_counts()
        co_occurrence = Counter()

        for _, row in df.iterrows():
            tags_in_row = row['tags'].split(';')
            filtered_tags_in_row = [tag for tag in tags_in_row if tag in teams or 'transaction' in tag.lower()]
            co_occurrence.update(combinations(filtered_tags_in_row, 2))

        filtered_tags_df = tag_counts[tag_counts.index.isin(teams) | tag_counts.index.str.contains('transaction', case=False)].reset_index()
        filtered_tags_df.columns = ['Tag', 'Count']
        filtered_tags_df.to_csv('../data/tag_frequencies.csv', index=False)

        common_pairs = co_occurrence.most_common(10)
        co_occurrence_df = pd.DataFrame(common_pairs, columns=['Tag Pair', 'Co-occurrence Count'])
        co_occurrence_df.to_csv('../data/tag_co_occurrences.csv', index=False)

        print("Tag analysis completed.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except pd.errors.EmptyDataError as e:
        print(f"Empty DataFrame: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    start()
