from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)

  enrollments = db.relationship("Course", secondary='enrollments')


class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)


class enrollments(db.Model):
  __tablename__ = "enrollments"
  enrollement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
  ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


@app.route("/", methods=['GET'])
def index():
  students = db.session.query(Student).all()
  print(students)
  # return render_template('no found.html')
  return render_template('index.html', students=students)


@app.route("/student/create", methods=['GET'])
def show_create_student():
  return render_template('student_create.html')


@app.route("/student/create", methods=['POST'])
def create_student():
  print(request.form)
  roll_no = request.form.get('roll')
  f_name = request.form.get('f_name')
  l_name = request.form.get('l_name')
  courses = request.form.getlist('courses')
  courses = [int(course.split('_')[1]) for course in courses]

  db.session.begin()
  try:
    students = db.session.query(Student).filter(Student.roll_number == roll_no).all()
    print('>>', students, '<<')

    if len(students) > 0:
      raise Exception("Already Found")

    new_student = Student(roll_number=roll_no, first_name=f_name, last_name=l_name)
    db.session.add(new_student)
    db.session.flush()

    enrollments = db.session.query(Course).filter(Course.course_id.in_(courses)).all()
    print('enrollments ', enrollments)
    for e in enrollments:
      new_student.enrollments.append(e)
  except Exception as e:
    print(e)
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  print(roll_no, f_name, l_name, courses)
  # return render_template('alreadyexists.html')
  return redirect(url_for('index'))


@app.route("/student/<student_id>", methods=['GET'])
def show_student(student_id):
  student = db.session.query(Student).filter(Student.student_id == student_id).one()
  print(student)
  print(student.enrollments)
  return render_template('student_details.html', student=student)


@app.route("/student/<student_id>/update", methods=['GET'])
def show_update_student(student_id):
  student = db.session.query(Student).filter(Student.student_id == student_id).one()
  print(student)
  return render_template('student_update.html', student=student)


@app.route("/student/<student_id>/update", methods=['POST'])
def update_student(student_id):
  print(request.form)
  f_name = request.form.get('f_name')
  l_name = request.form.get('l_name')
  courses = request.form.getlist('courses')
  courses = [int(course.split('_')[1]) for course in courses]

  db.session.begin()
  try:
    student = db.session.query(Student).filter(Student.student_id == student_id).one()

    print('>> student', student, '<<')
    print('>> student.enrollments', student.enrollments)

    student.first_name = f_name
    student.last_name = l_name
    student.enrollments = []

    enrollments = db.session.query(Course).filter(Course.course_id.in_(courses)).all()
    print('enrollments ', enrollments)
    for e in enrollments:
      student.enrollments.append(e)
  except Exception as e:
    print(e, ">>")
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('index'))


@app.route("/student/<student_id>/delete", methods=['GET'])
def delete_student(student_id):
  db.session.begin()
  try:
    student = db.session.query(Student).filter(Student.student_id == student_id).one()
    db.session.delete(student)
  except Exception as e:
    print(e, ">>")
    db.session.rollback()
  else:
    print('commiting')
    db.session.commit()

  return redirect(url_for('index'))

app.debug = True
if __name__ == "__main__":
  app.run(port=8000)
