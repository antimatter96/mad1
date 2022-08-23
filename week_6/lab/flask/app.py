from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from werkzeug.exceptions import HTTPException
from flask import make_response

import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_database.sqlite3"

db = SQLAlchemy()

db.init_app(app)
api = Api(app)
app.app_context().push()


class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)

  enrollments = db.relationship("Course", secondary='enrollment')


class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)


class Enrollment(db.Model):
  __tablename__ = "enrollment"
  enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
  course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


#####


class NotFoundError(HTTPException):

  def __init__(self, status_code):
    self.response = make_response('', status_code)


class BusinessValidationError(HTTPException):

  def __init__(self, status_code, error_code, error_message):
    data = {"error_code": error_code, "error_message": error_message}
    self.response = make_response(json.dumps(data), status_code)


##############

course_resource_fields = {
    "course_id": fields.Integer,
    "course_name": fields.String,
    "course_code": fields.String,
    "course_description": fields.String,
}

course_update_parser = reqparse.RequestParser()
course_update_parser.add_argument('course_name')
course_update_parser.add_argument('course_code')
course_update_parser.add_argument('course_description', type=str)

course_create_parser = course_update_parser.copy()

Course_Errors = {
    "COURSE001": "Course Name is required and should be string.",
    "COURSE002": "Course Code is required and should be string.",
    "COURSE003": "Course Description should be string.",
    "COURSE004": "Course Code is already assigned to other course."
}


class CourseAPI(Resource):

  @marshal_with(course_resource_fields)
  def get(self, course_id):
    print("CourseAPI Get")
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
      raise NotFoundError(status_code=404)
    return course, 200

  def delete(self, course_id):
    print("CourseAPI Delete")
    db.session.begin()
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
      raise NotFoundError(status_code=404)

    try:
      db.session.delete(course)
    except Exception as e:
      db.session.rollback()
      return '', 500
    else:
      db.session.commit()
    return '', 200

  @marshal_with(course_resource_fields)
  def put(self, course_id):
    print("CourseAPI PUT")
    args = course_update_parser.parse_args()

    course_name = args.get('course_name', None)
    course_code = args.get('course_code', None)
    course_description = args.get('course_description', '')

    if course_name is None:
      raise BusinessValidationError(status_code=400, error_code='COURSE001', error_message=Course_Errors['COURSE001'])

    if course_code is None:
      raise BusinessValidationError(status_code=400, error_code='COURSE002', error_message=Course_Errors['COURSE002'])

    db.session.begin()
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
      raise NotFoundError(status_code=404)
    any_other_course = db.session.query(Course).filter(Course.course_code == course_code, Course.course_id != course_id).first()
    if any_other_course is not None:
      raise BusinessValidationError(status_code=409, error_code='COURSE003', error_message=Course_Errors['COURSE004'])

    course.course_name = course_name
    course.course_code = course_code
    course.course_description = course_description

    try:
      db.session.add(course)
    except Exception as e:
      db.session.rollback()
      return '', 500
    else:
      print("CourseAPI PUT", 'commiting')
      db.session.commit()

    return course, 200

  @marshal_with(course_resource_fields)
  def post(self):
    print("CourseAPI POST")

    args = course_create_parser.parse_args()

    course_name = args.get('course_name', None)
    course_code = args.get('course_code', None)
    course_description = args.get('course_description', '')

    if course_name is None:
      raise BusinessValidationError(status_code=400, error_code='COURSE001', error_message=Course_Errors['COURSE001'])

    if course_code is None:
      raise BusinessValidationError(status_code=400, error_code='COURSE002', error_message=Course_Errors['COURSE002'])

    db.session.begin()
    any_other_course = db.session.query(Course).filter(Course.course_code == course_code).first()
    if any_other_course is not None:
      raise BusinessValidationError(status_code=409, error_code='COURSE004', error_message=Course_Errors['COURSE004'])

    course = Course(course_code=course_code, course_name=course_name, course_description=course_description)

    try:
      db.session.add(course)
    except Exception as e:
      db.session.rollback()
      return '', 500
    else:
      db.session.commit()

    return course, 201


##############

student_resource_fields = {
    "student_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "roll_number": fields.String,
}

student_update_parser = reqparse.RequestParser()
student_update_parser.add_argument('first_name')
student_update_parser.add_argument('last_name')
student_update_parser.add_argument('roll_number')

student_create_parser = student_update_parser.copy()

Student_Errors = {
    "STUDENT001": "Roll Number required and should be String",
    "STUDENT002": "First Name is required and should be String",
    "STUDENT003": "Last Name is String",
    "STUDENT004": "Student Roll Number is already assigned to other student"
}


class StudentAPI(Resource):

  @marshal_with(student_resource_fields)
  def get(self, student_id):
    print("StudentAPI Get")
    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
      raise NotFoundError(status_code=404)
    return student, 200

  def delete(self, student_id):
    print("StudentAPI Delete")
    db.session.begin()

    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
      raise NotFoundError(status_code=404)

    try:
      db.session.delete(student)
    except Exception as e:
      db.session.rollback()
      return '', 500
    else:
      db.session.commit()

    return '', 200

  @marshal_with(student_resource_fields)
  def put(self, student_id):
    args = student_update_parser.parse_args()

    first_name = args.get('first_name', None)
    roll_number = args.get('roll_number', None)
    last_name = args.get('last_name', None)

    if roll_number is None:
      raise BusinessValidationError(status_code=400, error_code='STUDENT001', error_message=Student_Errors['STUDENT001'])

    if first_name is None:
      raise BusinessValidationError(status_code=400, error_code='STUDENT002', error_message=Student_Errors['STUDENT002'])

    db.session.begin()
    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
      raise NotFoundError(status_code=404)

    any_other_student = db.session.query(Student).filter(Student.roll_number == roll_number, Student.student_id != student_id).first()
    if any_other_student is not None:
      raise BusinessValidationError(status_code=409, error_code='STUDENT004', error_message=Student_Errors['STUDENT004'])

    student.first_name = first_name
    student.roll_number = roll_number
    student.last_name = last_name

    try:
      db.session.add(student)
    except Exception as e:
      db.session.rollback()
      return 500
    else:
      print("CourseAPI PUT", 'commiting')
      db.session.commit()

    return student, 200

  @marshal_with(student_resource_fields)
  def post(self):
    args = student_update_parser.parse_args()

    first_name = args.get('first_name', None)
    roll_number = args.get('roll_number', None)
    last_name = args.get('last_name', None)

    if roll_number is None:
      raise BusinessValidationError(status_code=400, error_code='STUDENT001', error_message=Student_Errors['STUDENT001'])

    if first_name is None:
      raise BusinessValidationError(status_code=400, error_code='STUDENT002', error_message=Student_Errors['STUDENT002'])

    db.session.begin()
    any_other_student = db.session.query(Student).filter(Student.roll_number == roll_number).first()
    if any_other_student is not None:
      raise BusinessValidationError(status_code=409, error_code='STUDENT004', error_message=Student_Errors['STUDENT004'])

    student = Student(first_name=first_name, last_name=last_name, roll_number=roll_number)

    try:
      db.session.add(student)
    except Exception as e:
      db.session.rollback()
      return 500
    else:
      print("CourseAPI PUT", 'commiting')
      db.session.commit()

    return student, 201


##################################

enrollment_resource_fields = {
    "enrollment_id": fields.Integer,
    "student_id": fields.Integer,
    "course_id": fields.Integer,
}

enrollment_create_parser = reqparse.RequestParser()
enrollment_create_parser.add_argument('course_id')

Enrollment_Errors = {
    "ENROLLMENT001": "Course does not exist",
    "ENROLLMENT002": "Student does not exist.",
    "ENROLLMENT003": "Course Code is required and should be string.",
}


class EnrollmentAPI(Resource):

  @marshal_with(enrollment_resource_fields)
  def get(self, student_id):
    print("EnrollmentAPI Get")
    enrollments = db.session.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    if enrollments is None:
      raise NotFoundError(status_code=404)
    return enrollments

  def delete(self, student_id, course_id=None):
    print("EnrollmentAPI Delete")
    db.session.begin()

    if course_id == None:
      raise NotFoundError(status_code=404)

    enrollment = db.session.query(Enrollment).filter(Enrollment.student_id == student_id, Enrollment.course_id == course_id).first()

    if enrollment is None:
      raise NotFoundError(status_code=404)

    try:
      db.session.delete(enrollment)
    except Exception as e:
      db.session.rollback()
    else:
      print("StudentAPI Delete", 'commiting')
      db.session.commit()

    return '', 200

  @marshal_with(enrollment_resource_fields)
  def post(self, student_id):
    args = enrollment_create_parser.parse_args()

    course_id = args.get('course_id', None)

    if course_id is None:
      raise BusinessValidationError(status_code=400, error_code='ENROLLMENT003', error_message=Enrollment_Errors['ENROLLMENT003'])

    db.session.begin()
    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
      raise BusinessValidationError(status_code=404, error_code='ENROLLMENT002', error_message=Enrollment_Errors['ENROLLMENT002'])
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
      raise BusinessValidationError(status_code=400, error_code='ENROLLMENT001', error_message=Enrollment_Errors['ENROLLMENT001'])

    enrollment = Enrollment(student_id=student_id, course_id=course_id)

    try:
      db.session.add(enrollment)
    except Exception as e:
      db.session.rollback()
      return '', 500
    else:
      print("CourseAPI PUT", 'commiting')
      db.session.commit()

    return enrollment, 201


##############

api.add_resource(EnrollmentAPI, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")
api.add_resource(StudentAPI, "/api/student", "/api/student/<int:student_id>")
api.add_resource(CourseAPI, "/api/course", "/api/course/<int:course_id>")

###########

app.debug = True
if __name__ == "__main__":
  app.run(port=5000)
