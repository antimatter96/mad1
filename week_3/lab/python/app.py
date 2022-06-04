import sys
import csv

from jinja2 import Template
from matplotlib import pyplot as plt

ERROR_HTML_TEMPLATE_string = """
<!DOCTYPE html>
<html>
<header>
  <title>Something Went Wrong</title>
</header>
<body>
  <div id="header">
    <h1>Wrong Inputs</h1>
  </div>
  <div id="main">
    Something went wrong
  </div>
  <div id="footer">

  </div>
</body>
</html>
"""
ERROR_HTML_TEMPLATE = Template(ERROR_HTML_TEMPLATE_string)


STUDENT_DETAILS_TEMPLATE_string = """
<!DOCTYPE html>
<html>
<header>
  <title>Student Data</title>
</header>
<body>
  <style>
    table {
      border-collapse: collapse;
      border: 2px solid rgb(200,200,200);
    }
    td, th {
      border: 1px solid rgb(190,190,190);
      padding: 5px 10px;
    }
  </style>
  <div id="header">
    <h1>Student Details</h1>
  </div>
  <div id="main">
    <table>
      <thead>
        <tr>
          <th>Student id</th>
          <th>Course id</th>
          <th>Marks</th>
        </tr>
      </thead>
      <tbody>
        {% for course_marks in data %}
        <tr>
          <td>{{ course_marks["student_id"] }}</td>
          <td>{{ course_marks["course_id"] }}</td>
          <td>{{ course_marks["marks"] }}</td>
        </tr>
        {% endfor %}
      </tbody>
      <tfoot>
        <tr>
          <td colspan="2">Total Marks</td>
          <td>{{ total_marks }}</td>
        </tr>
      </tfoot>
    </table>
  </div>
  <div id="footer">

  </div>
</body>
</html>
"""
STUDENT_DETAILS_TEMPLATE = Template(STUDENT_DETAILS_TEMPLATE_string)


COURSE_DETAILS_TEMPLATE_string = """
<!DOCTYPE html>
<html>
<header>
  <title>Course Data</title>
</header>
<body>
  <style>
    table {
      border-collapse: collapse;
      border: 2px solid rgb(200,200,200);
    }
    td, th {
      border: 1px solid rgb(190,190,190);
      padding: 5px 10px;
    }
  </style>
  <div id="header">
    <h1>Course Details</h1>
  </div>
  <div id="main">
    <table>
      <tr>
        <td>Average Marks</td>
        <td>Maximum Marks</td>
      </tr>
      <tr>
        <td>{{ avg_marks }}</td>
        <td>{{ max_marks }}</td>
      </tr>
    </table>
    <img src="graph.png">
  </div>
  <div id="footer">
  </div>
</body>
</html>
"""
COURSE_DETAILS_TEMPLATE = Template(COURSE_DETAILS_TEMPLATE_string)


###########


_KEY_STUDENT_ID = 'Student id'
_KEY_COURSE_ID = 'Course id'
_KEY_MARKS = 'Marks'

KEY_STUDENT_ID = 'student_id'
KEY_COURSE_ID = 'course_id'
KEY_MARKS = 'marks'


def get_data():
    return read_csv("data.csv")


def read_csv(file_name):
    whole_data = []
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            whole_data.append({
                KEY_MARKS: row[_KEY_MARKS],
                KEY_COURSE_ID: row[_KEY_COURSE_ID],
                KEY_STUDENT_ID: row[_KEY_STUDENT_ID],
            })
    return whole_data


def filtered_data(data, key, value):
    filtered_data = []
    for d in data:
        if d[key] == value:
            filtered_data.append(d)
    return filtered_data

#############


def print_file(output):
    f = open('output.html', 'w')
    f.write(output)
    f.close()

#######


def print_error():
    error_html = ERROR_HTML_TEMPLATE.render()
    print_file(error_html)


def print_student_details(student_id):
    data = filtered_data(get_data(), KEY_STUDENT_ID, student_id)

    if len(data) == 0:
        print_error()
        return

    total_marks = sum([int(d[KEY_MARKS]) for d in data])

    student_html = STUDENT_DETAILS_TEMPLATE.render(
        data=data, total_marks=total_marks)
    print_file(student_html)


def print_course_details(course_id):
    data = filtered_data(get_data(), KEY_COURSE_ID, course_id)

    if len(data) == 0:
        print_error()
        return

    marks = [int(d[KEY_MARKS]) for d in data]

    plt.hist(marks)
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('graph.png')

    max_marks = max(marks)
    avg_marks = sum(marks)/len(marks)

    course_html = COURSE_DETAILS_TEMPLATE.render(
        avg_marks=avg_marks, max_marks=max_marks)
    print_file(course_html)

############


def main():
    if len(sys.argv) < 3:
        print_error()
        return

    if sys.argv[1] == "-s":
        print_student_details(sys.argv[2])
    elif sys.argv[1] == "-c":
        print_course_details(sys.argv[2])
    else:
        print_error()


if __name__ == "__main__":
    main()
