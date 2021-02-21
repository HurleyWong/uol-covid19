# Scrapes UoL coronavirus stats page and outputs data to a CSV file

import csv
import requests
from datetime import datetime
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from flask import Flask, request
import json

URL = "https://coronavirus.leeds.ac.uk/statistics-and-support-available/"

app = Flask(__name__)


@app.route("/latest", methods=["GET"])
def getLatestCase():
    """
    获得最近的日期的 case
    :return:
    """
    # 默认返回的内容格式
    return_dict = {
        'status_code': '200',
        'status_info': 'success',
        'result': {
            'Date': False,
            'Staff': False,
            'Students': False,
            'Other': False,
            'Total': False,
        }
    }

    table = extract_table()
    data = extract_data(table)
    index = len(data) - 1
    return_dict['result']['Date'] = data[index][0]
    return_dict['result']['Staff'] = data[index][1]
    return_dict['result']['Students'] = data[index][2]
    return_dict['result']['Other'] = data[index][3]
    return_dict['result']['Total'] = data[index][4]

    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/days", methods=["GET"])
def getDaysCase():
    """
    获得最近几天的 case
    """
    # 默认返回的内容格式
    return_dict = {
        'status_code': '200',
        'status_info': 'success',
        'result': []
    }

    table = extract_table()
    data = extract_data(table)

    count = len(data)

    result = []
    for i in range(count):
        result.append(
            {
                'Date': False,
                'Staff': False,
                'Students': False,
                'Other': False,
                'Total': False,
            })

        result[i]['Date'] = data[i][0]
        result[i]['Staff'] = data[i][1]
        result[i]['Students'] = data[i][2]
        result[i]['Other'] = data[i][3]
        result[i]['Total'] = data[i][4]

    return_dict['result'] = result

    return json.dumps(return_dict, ensure_ascii=False)


def extract_table():
    """
    提取表格
    :return:
    """
    request = requests.get(URL, headers={
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"
    })

    doc = BeautifulSoup(request.text, "html.parser")
    table = doc.find("table")

    # Sanity check that this is the table we want
    prev_element = table.find_parent().find_previous_sibling()
    assert prev_element.name == "p"
    text = str(prev_element.string).lower()
    assert text.startswith("confirmed coronavirus cases")

    return table


def extract_data(table):
    """
    提取数据
    :param table:
    :return:
    """
    rows = table.find_all("tr")
    assert len(rows) == 5

    dates = rows[0].find_all("td")
    staff_counts = rows[1].find_all("td")
    student_counts = rows[2].find_all("td")
    other_counts = rows[3].find_all("td")
    totals = rows[4].find_all("td")
    # 工作人员总数
    assert len(dates) == len(staff_counts)
    # 学生总数
    assert len(staff_counts) == len(student_counts)
    # 其他人总数
    assert len(student_counts) == len(other_counts)
    # 所有人总数
    assert len(other_counts) == len(totals)

    data = []
    for i in range(1, len(dates)):
        dt = datetime.strptime(dates[i].string, "%d %b %Y")
        data.append((dt.date().isoformat(), staff_counts[i].string,
                     student_counts[i].string, other_counts[i].string,
                     totals[i].string))

    return data


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
    app.run(debug=True)

# if __name__ == "__main__":
#     args = parse_command_line()
#
#     table = extract_table()
#     data = extract_data(table)
#
#     count = len(data)
#
#     print(len(data))
#     print(data[index])
#
#     if args.update:
#         update_csv(data, args.filename)
#     else:
#         write_csv(data, args.filename)
