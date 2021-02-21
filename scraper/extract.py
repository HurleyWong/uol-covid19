import requests
from bs4 import BeautifulSoup
from datetime import datetime


def extract_table(URL):
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
