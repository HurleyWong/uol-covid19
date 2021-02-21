from flask import Flask, request
import json
from scraper.extract import *

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

    table = extract_table(URL)
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


if __name__ == "__main__":
    app.run(debug=True)