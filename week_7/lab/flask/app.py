# ╔════════════════════════════════════════════════════╦════════╦════════════════════════════════════════════════════════════════╦
# ║ /                                                  ║ get    ║ table+button                                                   ║
# ║ /student/create                                    ║ get    ║ form                                                           ║
# ║ /student/create                                    ║ post   ║ add, redirect to /                                             ║
# ║                                                    ║        ║  no add -> show error, go back button                          ║
# ║ /student/<int:student id>/update                   ║ get    ║ form                                                           ║
# ║ /student/<int:student id>/update                   ║ post   ║ update, DO NOT DELETE OLD ONES, redirect                       ║
# ║ /student/<int:student id>/delete                   ║ get    ║ delete, student, enrollments, redirect                         ║
# ║ /student/<int:student id>                          ║ get    ║ 2 tables [student + enroll [only if enrollments]] + go back    ║
# ║                                                    ║        ║ table with withdraw button                                     ║
# ║ /student/<int:student id>/withdraw/<int:course id> ║ get    ║ remove , redirect                                              ║
# ║                                                    ║        ║                                                                ║
# ║                                                    ║        ║                                                                ║
# ║ /courses                                           ║ get    ║ show table courses[ show message if none, go to students page] ║
# ║ /course/create                                     ║ get    ║ form                                                           ║
# ║ /course/create                                     ║ post   ║ create, redirect                                               ║
# ║ .                                                  ║ .      ║ exists -> show error, button                                   ║
# ║ /course/<int:course id>/update                     ║ get    ║ form                                                           ║
# ║ /course/<int:course id>/update                     ║ post   ║ update, redirect                                               ║
# ║ /course/<int:course id>/delete                     ║ get    ║ delete, redirect                                               ║
# ║ /course/<int:course id>                            ║ get    ║ 2 tables[course + enrollments]                                 ║
# ╚════════════════════════════════════════════════════╩════════╩════════════════════════════════════════════════════════════════╩

from calendar import c
from crypt import methods
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///week7_database.sqlite3"

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

## MODELS

class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)

  enrollments = db.relationship("Course", secondary='enrollments', back_populates="students")

class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)

  students = db.relationship("Student", secondary='enrollments', back_populates="enrollments")

class enrollments(db.Model):
  __tablename__ = "enrollments"
  enrollement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
  ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

## ROUTES

@app.route("/", methods=['GET'])
def list_students():
  return _list_students()

@app.route("/student/create", methods=['GET'])
def show_create_student():
  return _show_create_student()

@app.route("/student/create", methods=['POST'])
def create_student():
  return _create_student()

@app.route("/student/<student_id>/update", methods=['GET'])
def show_update_student(student_id):
  return _show_update_student(student_id)

@app.route("/student/<student_id>/update", methods=['POST'])
def update_student(student_id):
  return _update_student(student_id)

@app.route("/student/<student_id>/delete", methods=['GET'])
def delete_student(student_id):
  return _delete_student(student_id)

@app.route("/student/<student_id>", methods=['GET'])
def show_student_details(student_id):
  return _show_student_details(student_id)

@app.route("/student/<student_id>/withdraw/<course_id>", methods=['GET'])
def withdraw_course(student_id, course_id):
  return _withdraw_course(student_id, course_id)

#

@app.route("/courses", methods=['GET'])
def list_courses():
  return _list_courses()

@app.route("/course/create", methods=['GET'])
def show_create_course():
  return _show_create_course()

@app.route("/course/create", methods=['POST'])
def create_course():
  return _create_course()

@app.route("/course/<course_id>/update", methods=['GET'])
def show_update_course(course_id):
  return _show_update_course(course_id)

@app.route("/course/<course_id>/update", methods=['POST'])
def update_course(course_id):
  return _update_course(course_id)

@app.route("/course/<course_id>/delete", methods=['GET'])
def delete_course(course_id):
  return _delete_course(course_id)

@app.route("/course/<course_id>", methods=['GET'])
def show_course_details(course_id):
  return _show_course_details(course_id)

## CONTROLLERS

def _list_students():
  students = db.session.query(Student).all()
  print(students)
  return render_template('students.html', students=students)

def _show_create_student():
  return render_template('student_add_form.html')

def _create_student():
  print(request.form)
  roll_no = request.form.get('roll')
  f_name = request.form.get('f_name')
  l_name = request.form.get('l_name')

  db.session.begin()
  try:
    students = db.session.query(Student).filter(Student.roll_number == roll_no).all()

    if len(students) > 0:
      raise Exception("Already Found")

    new_student = Student(roll_number=roll_no, first_name=f_name, last_name=l_name)
    db.session.add(new_student)
  except Exception as e:
    print(e)
    db.session.rollback()
    return render_template('student_exists_error.html')
  else:
    print('commiting')
    db.session.commit()

  print(roll_no, f_name, l_name)

  return redirect(url_for('list_students'))

def _show_update_student(student_id):
  student = db.session.query(Student).filter(Student.student_id == student_id).first()
  all_courses = db.session.query(Course).all()
  return render_template('student_update_form.html', student=student, all_courses=all_courses)

def _update_student(student_id):
  print(request.form)
  f_name = request.form.get('f_name')
  l_name = request.form.get('l_name')
  course_id = request.form.get('course')

  print(course_id)
  db.session.begin()
  try:
    student = db.session.query(Student).filter(Student.student_id == student_id).one()

    student.first_name = f_name
    student.last_name = l_name

    course = db.session.query(Course).filter(Course.course_id == course_id).first()

    student.enrollments.append(course)
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  print(f_name, l_name)

  return redirect(url_for('list_students'))

def _delete_student(student_id):
  db.session.begin()
  try:
    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    db.session.delete(student)
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('list_students'))

def _show_student_details(student_id):
  student = db.session.query(Student).filter(Student.student_id == student_id).first()
  return render_template('student_details.html', student=student)

def _withdraw_course(student_id, course_id):
  print(request.form)
  db.session.begin()
  try:
    student = db.session.query(Student).filter(Student.student_id == student_id).one()
    course = db.session.query(Course).filter(Course.course_id == course_id).first()

    student.enrollments.remove(course)
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('list_students'))

def _list_courses():
  courses = db.session.query(Course).all()
  return render_template('courses.html', courses=courses)

def _show_create_course():
  return render_template('course_add_form.html')

def _create_course():
  print(request.form)
  code = request.form.get('code')
  name = request.form.get('c_name')
  description = request.form.get('desc')

  db.session.begin()
  try:
    courses = db.session.query(Course).filter(Course.course_code == code).all()

    if len(courses) > 0:
      raise Exception("Already Found")

    new_course = Course(course_code=code, course_name=name, course_description=description)
    db.session.add(new_course)
  except Exception as e:
    print(e)
    db.session.rollback()
    return render_template('course_exists_error.html')
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('list_courses'))

def _show_update_course(course_id):
  course = db.session.query(Course).filter(Course.course_id == course_id).first()
  return render_template('course_update_form.html', course=course)

def _update_course(course_id):
  print(request.form)
  course_name = request.form.get('c_name')
  course_description = request.form.get('desc')

  print(course_id)
  db.session.begin()
  try:
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    course.course_name = course_name
    course.course_description = course_description
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  print(course_name, course_description)

  return redirect(url_for('list_courses'))

def _delete_course(course_id):
  db.session.begin()
  try:
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    db.session.delete(course)
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('list_students'))

def _show_course_details(course_id):
  course = db.session.query(Course).filter(Course.course_id == course_id).first()
  return render_template('course_details.html', course=course)

app.debug = True
if __name__ == "__main__":
  app.run(port=8000)
