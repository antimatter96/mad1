# ORM
# Can use classes to use db

from datetime import datetime
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import select

from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

## Models

Base = declarative_base()

## class name could be anything


class User(Base):
  __tablename__ = 'user'    ## same as in db

  ## same name as in db
  user_id = Column(Integer, autoincrement=True, primary_key=True)
  username = Column(String, unique=True)
  email = Column(String, unique=True)

  ## articles = relationship("Article", secondary='article_authors')


class Article(Base):
  __tablename__ = 'article'    ## same as in db

  ## same name as in db
  article_id = Column(Integer, autoincrement=True, primary_key=True)
  title = Column(String)
  content = Column(String)

  authors = relationship("User", secondary='article_authors')


class ArticleAuthors(Base):
  __tablename__ = 'article_authors'    ## same as in db

  user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True, nullable=False)
  article_id = Column(Integer, ForeignKey("article.article_id"), primary_key=True, nullable=False)


# dialet+drivef://unam:pa@hos:port/db

engine = create_engine("sqlite:///./test1db.sqlite3")

# if __name__ == '__main__':
#   stmt = select(User)

#   print('//QUERY--\n', stmt, '\n\\\\')

#   with engine.connect() as conn:
#     print('--RESULT--')
#     rows = conn.execute(stmt)
#     for row in rows:
#       print(row)

## do not get connection everytine
## create a session
## use this session
## represents holding zone

# if __name__ == '__main__':
#   with Session(engine) as session:
#     articles = session.query(Article).filter(Article.article_id == 2).all()

#     for article in articles:
#       print(article.title)

#       for author in article.authors:
#         print('\t by', author.username)

# AND
# from sqlaclchmey import and_
#
# query.filter( and_(x=='A', Y=='B') )
# query.filter(x=='A', Y=='B')
# query.filter(x=='A').filter(Y=='B')
#

# OR
# from sqlaclchmey import or_
#
# query.filter( or_(x=='A', Y=='B') )
#

# .one()
# .all()

# JOIN
# for u, a in session.query(
#     User, Address).filter(User.user_id == Address.article_id).filter(Address.city == '').all():
#   print(u, a)
#
#
# query.join(Address, User.user_id == Address.user_id)
# query.join(User.addresses) ## 
# query.join(Address, User.addresses)
# query.join( User.addresses.and_(Address.city=='') ) # set condtion at ON
#
# query.outerjoin(User.addresses)
#


## Transactions


if __name__ == '__main__':
  with Session(engine, autoflush=False) as session:
    session.begin()
    try:
      article = Article(title= "Title - " + datetime.today().isoformat() + "", content= datetime.today().isoformat() + " content")
      session.add(article)
      session.flush() # to get articlre_id


      print(article.article_id, article.title)

      article_authors = ArticleAuthors(user_id = 1, article_id = article.article_id)
      session.add(article_authors)

      # print(1/0)
    except:
      print("roll back")
      session.rollback()
      raise
    else:
      print("commit")
      session.commit()


if __name__ == '__main__':
  with Session(engine, autoflush=False) as session:
    session.begin()
    try:
      author = session.query(User).filter(User.user_id==2).one()
      article = Article(title= "Title - " + datetime.today().isoformat() + "", content= datetime.today().isoformat() + " content")
      article.authors.append(author)

      session.add(article)
    except:
      print("roll back")
      session.rollback()
      raise
    else:
      print("commit")
      session.commit()


if __name__ == '__main__':
  with Session(engine, autoflush=False) as session:
    session.begin()
    try:
      author1 = session.query(User).filter(User.user_id==2).one()
      author2 = session.query(User).filter(User.user_id==1).one()
      article = Article(title= "Title - " + datetime.today().isoformat() + "", content= datetime.today().isoformat() + " content")
      article.authors.append(author1)
      article.authors.append(author2)

      session.add(article)
      # session.flush()
      # print(article.article_id, article.title)
    except:
      print("roll back")
      session.rollback()
      raise
    else:
      print("commit")
      session.commit()
