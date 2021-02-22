# uol-covid19

This repository contains

* A CSV file of aggregated coronavirus case data scraped from [the University of Leeds website][uol]
* Python code for the scraper
* Python code to process and analyze the data

## Scraper Usage Examples

To scrape case data and write to a new file in the `scraper` folder:

`python daily-cases.py cases.csv`

or in the root folder:

`python scraper/daily-cases.py cases.csv`

To scrape case data and update an existing CSV file in the `scraper` folder:

`python daily-cases.py --update cases.csv`

or in the root folder:

`python scraper/daily-cases.py --update cases.csv`

Note: if the newly-scraped data contains records whose dates match existing
records, those existing records will be replaced by the new data.

## API

In order to make this project to fetch data via the API, the Flask framework has been added to this project to enable this. You can start the service by running the `extract.py` file and then get the number of cases for the latest date and the latest week in the following links:

* To get the cases of latest day, access `http://127.0.0.1:5000/latest` in your browser
* To get the cases of latest week, access `http://127.0.0.1:5000/days` in your browser

## Analysis Examples

To derive day-by-day active cases from a CSV file of daily case reports in the root folder:

`python analysis/active-cases.py data/2021-cases.csv`

This will display the active cases on screen as a table. To output the
active cases to a file, do:

`python analysis/active-cases.py -o data/2021-active.csv data/2021-cases.csv`


## Dependencies

* [Requests][req]
* [BeautifulSoup 4][bs]
* [Rich][rich] 9.0.0 or newer (not required for scraper)

To use the scripts, create and activate a Python 3 virtual environment,
then do:

`pip install -r requirements.txt`

or choose to install dependecies in this way:

```shell
pip install requests
pip install beautifulsoup4
pip install rich
```

[uol]: https://coronavirus.leeds.ac.uk/statistics-and-support-available/
[req]: https://requests.readthedocs.io/en/master/
[bs]: https://www.crummy.com/software/BeautifulSoup/
[rich]: https://rich.readthedocs.io/en/latest/introduction.html
