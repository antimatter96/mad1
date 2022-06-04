from flask import request
from flask import render_template
from flask import Flask
import csv

from jinja2 import Template
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
plt.ioff()

ERROR_HTML_TEMPLATE_string = """"""
ERROR_HTML_TEMPLATE = Template(ERROR_HTML_TEMPLATE_string)


STUDENT_DETAILS_TEMPLATE_string = """

"""
STUDENT_DETAILS_TEMPLATE = Template(STUDENT_DETAILS_TEMPLATE_string)


COURSE_DETAILS_TEMPLATE_string = """

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


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html.jinja2")
    if request.method == "POST":
        print(request.form)
        if request.form.get('ID') is not None and request.form.get('id_value') is not None:
            if request.form.get('ID') == 'student_id':
                student_id = request.form.get('id_value')
                data = filtered_data(get_data(), KEY_STUDENT_ID, student_id)

                if len(data) == 0:
                    return render_template("error.html.jinja2")

                total_marks = sum([int(d[KEY_MARKS]) for d in data])

                return render_template('student_details.html.jinja2', data=data, total_marks=total_marks)

            elif request.form.get('ID') == 'course_id':
                course_id = request.form.get('id_value')
                data = filtered_data(get_data(), KEY_COURSE_ID, course_id)

                if len(data) == 0:
                    return render_template("error.html.jinja2")

                marks = [int(d[KEY_MARKS]) for d in data]

                plt.hist(marks)
                plt.xlabel('Marks')
                plt.ylabel('Frequency')
                plt.savefig('./static/graph.png')
                plt.close()


                max_marks = max(marks)
                avg_marks = sum(marks)/len(marks)

                return render_template("course_details.html.jinja2", avg_marks=avg_marks, max_marks=max_marks)
            else:
                return render_template("error.html.jinja2")
        else:
            return render_template("error.html.jinja2")

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
