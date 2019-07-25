# conding=utf-8
import os
from datetime import timedelta, datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import time
import requests, re

# {"user":"root","passwd":"abcdefg","host":"2211.cc","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}
try:
    key = json.loads(open('key.json', 'r', encoding='utf-8').read())
except:
    s = '{"user":"user","passwd":"password","host":"host","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}'
    open('key.json', 'w', encoding='utf-8').write(s)
    print("编辑key.json")
    exit()
basedir = os.path.abspath(os.path.dirname(__file__))
mysql_config = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(key['user'], key['passwd'], key['host'], key['port'],
                                                                  key['dbname'], key['charset'])
sqlite_config = 'sqlite:///' + os.path.join(basedir, 'app.db')


# print(mysql_config)
class Config(object):
    # SECRET_KEY=key['secret_key']+str(os.urandom(24))
    SECRET_KEY = key['secret_key']
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)
    # 设置session的保存时间。
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   sqlite_config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or mysql_config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


time.sleep(3)
static = './static'
template_folder = './templates'
app = Flask(__name__, static_folder=static, template_folder=template_folder, )
app.config.from_object(Config)
base_path_dir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)


# db config model
class as_info_DB(db.Model):
    __tablename__ = 'asinfodb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asid = db.Column(db.String(512), nullable=True, comment="")
    ips = db.Column(db.String(512), nullable=True, comment="")
    company = db.Column(db.String(512), nullable=True, comment="")
    number = db.Column(db.String(512), nullable=True, comment="")
    uptime = db.Column(db.DateTime, index=True, default=datetime.now)
    __table_args__ = {
        "mysql_charset": "utf8"
    }


class src_DB(db.Model):
    __tablename__ = 'srcdb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512), nullable=True, comment="")
    content = db.Column(db.Text, nullable=True, comment="")
    title = db.Column(db.String(512), nullable=True, comment="")
    uptime = db.Column(db.DateTime, index=True, default=datetime.now)

    __table_args__ = {
        "mysql_charset": "utf8"
    }


# web route
@app.route("/", endpoint="index")
def index():
    return "web is run"


# app logic

# 定义访问url
class url():
    index = "https://www.yuhuashi.info/"
    page = "https://www.yuhuashi.info/page_{}.html"
    link = ""


# 定义过滤规则
class r_re():
    r_link = re.compile(r'class="post-title"><a href="(.*?)">')
    r_title = re.compile(r'<title>雨花石-(.*?)</title>')
    r_body = re.compile(r'<div class="post-body">(.*?)<nav class="article-nav">', re.S)


# 爬取抓取的连接，使用正则提取需要爬取的页面。
def get_link_to_db():
    for i in range(1, 12):
        if i == 1:
            gurl = url.index
        else:
            gurl = url.page.format(i)
        src = requests.get(gurl)
        text = src.content.decode()
        link_arr = r_re.r_link.findall(str(text))
        for i in link_arr:
            idb = src_DB()
            idb.url = i
            db.session.add(idb)
            db.session.commit()


# 从数据库获取爬取的连接爬取内容。并且 过滤
def get_content_to_db():
    dbs = src_DB.query.filter_by(content=None).all()
    # dbs=src_DB.query.filter_by(content="").first()
    for i in dbs:
        print(i.id)
        t_db = src_DB.query.filter_by(id=i.id).first()
        url = i.url
        t = requests.get(url).content.decode()
        t_db.content = r_re.r_body.findall(str(t))[0]  # 如果有图片，下载图片转换base64 替换插入

        t_db.title = r_re.r_title.findall(str(t))[0]
        # print(i)
        db.session.commit()
    pass


#提取标题和内容
def get_content(t):
    body = r_re.r_title.findall(str(t))[0]
    title = r_re.r_title.findall(str(t))[0]
    return body, title


# 提取内容图片连接，并且卸载转换成base64
def get_content_img(t):
    re_src=""
    src=""
    srcset=""
    pass

if __name__ == "__main__":
    pass
    # get_content_to_db()
    # app.run(debug=False)
