# conding=utf-8
import os
from datetime import timedelta, datetime
from flask import Flask, render_template,request
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





class dls_info_DB(db.Model):
    __tablename__ = 'dlsinfodb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True, comment="")
    dengji = db.Column(db.String(255), nullable=True, comment="")
    zk = db.Column(db.Float, default=1, comment="")
    qian = db.Column(db.Float,default=0, comment="")
    huokuan = db.Column(db.Float,default=0, comment="")
    updl = db.Column(db.Integer, default=0,  comment="")
    downdl = db.Column(db.String(4096), nullable=True, comment="")
    downdl_huokuan = db.Column(db.Float,default=0,comment="总计下级代理结余货款 发展的下线手上的货款")
    downdl_dslirun = db.Column(db.Float,default=0, comment="待收利润")
    downdl_huikuan = db.Column(db.Float,default=0, comment="总计下级代理销售")
    downdl_yslirun = db.Column(db.Float,default=0, comment="已收利润")
    downdl_txlirun = db.Column(db.Float,default=0, comment="提现利润")
    uptime = db.Column(db.DateTime, index=True, default=datetime.now)
    addname= db.Column(db.String(255), nullable=True, comment="")
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    status = db.Column(db.String(255), nullable=True, comment="")
    __table_args__ = {
        "mysql_charset": "utf8"
    }

class dls_log_DB(db.Model):
    __tablename__ = 'dlsdblog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255), nullable=True, comment="")
    something = db.Column(db.String(4096), nullable=True, comment="")
    sometime = db.Column(db.DateTime, index=True, default=datetime.now)
    __table_args__ = {
        "mysql_charset": "utf8"
    }

from suan.suan import daili
# web route
@app.route("/", endpoint="index")
def index():
    return "web is run"

def show_daili():

    pass

def add_daili():
    name="小王"
    updl=0
    dbs=dls_info_DB()
    dbs.name=name
    dbs.updl=request.args['id'] if "id" not in  request.args else updl
    db.session.add(dbs)
    db.session.commit()

    #代理名字
    #上级代理  当前登陆用户作为上级代理
    #下级代理
    # dbs = src_DB.query.filter_by(content=None).all()
    pass

def stop_daili():
    pass

def tui_daili():
    self=0
    if self==0: return "公司？？退?"
    dbs = dls_info_DB.query.filter_by(id=int(self)).first()
    tui_dl_qian = float('%.2f' % float(dbs.huokuan * dbs.zk))
    tui_zongzhang = tui_dl_qian + dbs.downdl_yslirun - dbs.downdl_txlirun

    #安排
    while 1:
        x_up_id=dbs.updl
        x_up_zk=dbs.zk
        db.session.commit()
        #逐级退待收利润
        if int(x_up_id)>0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()



    self.downdl_dslirun = self.downdl_dslirun + dslr
    print("存在的利润款{}".format(
        ((tui_xiadailiqian / self.zk * 10) - (tui_xiadailiqian / xiadailizhekou * 10)) / 10 * self.zk))

    selflr = tui_xiadailiqian - tui_xiadailiqian / xiadailizhekou * self.zk

    if self.has_updl:
        pass
    self.downdl_dslirun = float('%.2f' % float(self.downdl_dslirun - (
            ((tui_xiadailiqian / self.zk * 10) - (tui_xiadailiqian / xiadailizhekou * 10)) / 10 * self.zk)))
    self.downdl_huokuan = self.downdl_huokuan - xiadailihuokuan  # 总计下级代理结余货款 发展的下线手上的货款

    self.downdl_huikuan = float('%.2f' % float(self.downdl_huikuan))  # 总计下级代理销售



    self.downdl_huokuan = 0  # 总计下级代理结余货款 发展的下线手上的货款
    self.downdl_dslirun = 0  # 待收利润
    self.downdl_huikuan = 0  # 总计下级代理销售
    self.downdl_yslirun = 0  # 已收利润
    self.downdl_txlirun = 0  # 提现利润

    pass

def daili_chongqian():
    # 代理级别（折扣）=代理规则（钱）
    self=0
    chongqian=100
    pingguzhekou=""
    # 安排折扣
    dbs = dls_info_DB.query.filter_by(id=self).first()
    dbs.zk=0.7
    db.session.commit()
    dbs = dls_info_DB.query.filter_by(id=self).first()
    dbs.qian = float(dbs.qian) + float(chongqian)
    dbs.huokuan = dbs.huokuan + chongqian / dbs.zk

    #安排
    while 1:
        x_up_id=dbs.updl
        x_up_zk=dbs.zk
        db.session.commit()
        #利润安排
        if int(x_up_id)>0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            #安排代理商应收货款
            lr=(chongqian/dbs.zk-chongqian/x_up_zk) #上级代理折扣-现在代理折扣等于代理折扣利润
            dbs.downdl_huokuan=dbs.downdl_huokuan+lr# 总计下级代理结余货款 发展的下线手上的货款
            dbs.downdl_dslirun=dbs.downdl_dslirun+lr*dbs.zk# 待收利润
            # zjnh = float('%.2f' % float(dailiqian / self.zk * 10))  # dailiqian / (fxdailijbie_zk - self.zk) * 10
            # dlnh = float('%.2f' % float(dailiqian / fxdailijbie_zk * 10))
            # selflr = tui_xiadailiqian - tui_xiadailiqian / xiadailizhekou * self.zk
            pass
        else:
            break
    return "代理充钱分配完毕"

def daili_fazhandaili():
    pass


def buy():

    pass



if __name__ == "__main__":
    pass
    # get_content_to_db()
    app.run(debug=False)
