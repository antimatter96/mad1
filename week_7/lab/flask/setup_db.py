from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine('sqlite:///week7_database.sqlite3')
meta = MetaData()

student = Table(
    'student',
    meta,
    Column('student_id', Integer, primary_key=True, autoincrement=True),
    Column('roll_number', String, unique=True, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String),
)

course = Table(
    'course',
    meta,
    Column('course_id', Integer, primary_key=True, autoincrement=True),
    Column('course_code', String, unique=True, nullable=False),
    Column('course_name', String, nullable=False),
    Column('course_description', String),
)

enrollments = Table(
    'enrollments', meta, Column('enrollement_id', Integer, primary_key=True, autoincrement=True),
    Column('estudent_id', Integer, ForeignKey("student.student_id"), nullable=False),
    Column('ecourse_id', Integer, ForeignKey("course.course_id"), nullable=False)
)

try:
  meta.create_all(engine)
except Exception as e:
  print('Create Error', e)

try:
  engine.execute(course.insert(), course_code='CSE01', course_name='MAD I', course_description='Modern Application Development - I')
  engine.execute(course.insert(), course_code='CSE02', course_name='DBMS', course_description='Database management Systems')
  engine.execute(
      course.insert(), course_code='CSE03', course_name='PDSA', course_description='Programming, Data Structures and Algorithms using Python'
  )
  engine.execute(course.insert(), course_code='BST13', course_name='BDM', course_description='Business Data Management')
except Exception as e:
  print('Insert Error', e)

# course id course code course name course description
# 1 CSE01 MAD I Modern Application Development - I
# 2 CSE02 DBMS Database management Systems
# 3 CSE03 PDSA Programming, Data Structures and Algorithms using Python
# 4 BST13 BDM Business Data Management
