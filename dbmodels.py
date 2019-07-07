__author__ = 'yo'
# from flask_sqlalchemy import SQLAlchemy
# from . import db
from datetime import datetime
# class file_art(db.Model):
from sqlalchemy import Column, String, create_engine,Integer,Text,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker,scoped_session
# from sqlalchemy import create_engine
# engine = create_engine(DATABASE_URI, convert_unicode=True, pool_size=50, pool_recycle=3600)
# session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
# db.session = session()
#
# db = SQLAlchemy()

# 创建对象的基类:
Base = declarative_base()

def content_DB(Base):
    __tablename__ = 'contentdb'
    id=""
    title=""
    description=""
    keywords=""
    author=""
    content=""
    category=""
    counter=""
    date=""
    srcurl=""

def src_DB(Base):
    __tablename__ = 'srcdb'
    id=Column(Integer, primary_key=True, autoincrement=True)
    url=Column(String(512), nullable=True, comment="")
    content=Column(Text, nullable=True, comment="")
    title=Column(String(512), nullable=True, comment="")
    uptime=Column(DateTime, index=True, default=datetime.now)

    __table_args__ = {
        "mysql_charset": "utf8"
    }

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@host:3306/arts')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
# print 'type:', type(user)
# print 'name:', user.name
# 关闭Session:
session.close()