# MLB Rumors Crawler

This is a Python script that scrapes MLB trade rumors from the website [MLBTradeRumors.com](https://www.mlbtraderumors.com) using proxies for anonymity. It fetches the latest articles, extracts relevant information such as title, content, tags, date, and saves the data in a CSV file.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)
- ProxyBroker library (`pip install proxybroker`)

or

```bash
pip install -r requirements.txt
```

## How to Use

1. Clone this repository or download the `main.py` file.

2. Install the required libraries mentioned in the prerequisites.

3. Run the script using the command `python3 main.py`. The script will automatically search for usable proxies, clean them, and start scraping the MLB trade rumors.

4. The scraped data will be stored in a CSV file named `MLB_rumors.csv` (currently commented out in the code). You can uncomment the relevant lines to enable CSV file generation and customize the file name and format if needed.

## Important Note

Please be mindful of web scraping ethics and legal guidelines when using this script. Make sure to respect the website's terms of service, use proxies responsibly, and avoid excessive requests to prevent any potential disruption or misuse.

Feel free to modify the script to suit your specific needs or enhance its functionality.

Happy scraping!

## Credits
```
- Author: Shu-Hao Wu
- Email: shwu2@illinois.edu
```