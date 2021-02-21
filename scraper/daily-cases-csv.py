# Scrapes UoL coronavirus stats page and outputs data to a CSV file

import csv
from argparse import ArgumentParser
from extract import *

URL = "https://coronavirus.leeds.ac.uk/statistics-and-support-available/"


def write_csv(data, filename):
    """
    编写 csv
    :param data:
    :param filename:
    """
    with open(filename, "wt", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(("Date", "Staff", "Students", "Other", "Total"))
        writer.writerows(data)


def read_csv(filename):
    """
    读取 csv
    :param filename:
    :return:
    """
    with open(filename, "rt", newline="") as infile:
        reader = csv.reader(infile)
        return list(reader)[1:]


def update_csv(new_data, filename):
    """
    更新 csv
    :param new_data:
    :param filename:
    """
    current_by_date = {rec[0]: tuple(rec) for rec in read_csv(filename)}
    new_by_date = {rec[0]: rec for rec in new_data}
    merged_by_date = {**current_by_date, **new_by_date}
    merged = sorted(merged_by_date.values())
    write_csv(merged, filename)


def parse_command_line():
    """
    解析命令行
    :return:
    """
    parser = ArgumentParser(
        description="Scrapes UoL website and writes daily coronavirus cases to a CSV file."
    )
    parser.add_argument(
        "-u", "--update", action="store_true",
        help="use scraped data to update specified file"
    )
    parser.add_argument(
        "filename", metavar="FILENAME",
        help="name of CSV file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line()

    table = extract_table(URL)
    data = extract_data(table)


    if args.update:
        update_csv(data, args.filename)
    else:
        write_csv(data, args.filename)
