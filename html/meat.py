__author__ = 'yo'
#conding=utf-8

#conding=utf-8
import os
from datetime import timedelta,datetime
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json
# {"user":"root","passwd":"abcdefg","host":"2211.cc","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}
try:
    key=json.loads(open('key.json','r',encoding='utf-8').read())
except:
    s='{"user":"user","passwd":"password","host":"host","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}'
    open('key.json', 'w', encoding='utf-8').write(s)
    print("编辑key.json")
    exit()
basedir = os.path.abspath(os.path.dirname(__file__))
# o=("mysql+pymysql://root:s@ts:3306/t1?charset=utf8",echo=True,encoding='utf-8',convert_unicode=True)
mysql_config='mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(key['user'],key['passwd'],key['host'],key['port'],key['dbname'],key['charset'])
sqlite_config='sqlite:///' + os.path.join(basedir, 'app.db')
# print(mysql_config)
class Config(object):
    # SECRET_KEY=key['secret_key']+str(os.urandom(24))
    SECRET_KEY=key['secret_key']
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)
    # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
    # SECRET_KEY= os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
    # 设置session的保存时间。
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   sqlite_config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   mysql_config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

static='./static'
template_folder='./templates'
app=Flask(__name__, static_folder=static, template_folder=template_folder,)
app.config.from_object(Config)
base_path_dir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})#/api全局跨站

class meta_DB(db.Model):
    __tablename__ = 'metadb'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(512), nullable=True, comment="")
    content=db.Column(db.String(512), nullable=True, comment="")
    source_url=db.Column(db.String(512), nullable=True, comment="")
    uptime=db.Column(db.DateTime, index=True, default=datetime.now)

    __table_args__ = {
        "mysql_charset": "utf8"
    }

@app.route("/",endpoint="index")
def index():
    return "web is run"

from flask import Blueprint, render_template, redirect, request, session, flash ,jsonify
from flask_restful import Api, Resource,reqparse,abort


class To(Resource):
    def get(self,todo_id):

        return jsonify({'test_api': todo_id})
apis = Api(app)
apis.add_resource(To, '/ip/<todo_id>',endpoint='bb')

if __name__ == "__main__":
    pass
    app.run(debug=True)
