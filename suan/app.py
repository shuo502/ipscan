# conding=utf-8
import os
from datetime import timedelta, datetime
from flask import Flask, render_template,request,url_for
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
    zk = db.Column(db.Float, default=1.0, comment="")
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

# from suan.suan import daili
# web route
@app.route("/", endpoint="index")
def index():
    nav="""
    <a href="{}">查看<a><br>
    <a href="{}">增加代理<a><br>
    <a href="{}">退出代理<a><br>
    <a href="{}">增加钱<a><br>
    <a href="{}">购买<a><br>
    """.format(url_for('show'),url_for('add'),url_for('out'),url_for('addmoney'),url_for('buy'))
    dbs = dls_info_DB.query.filter_by().all()
    allus=""
    if dbs:
        for i in dbs:
            b=look(i)
            allus=allus+"{} <br>".format(b)
    else:
        allus="还没有代理商"

    return allus+nav

class f():
    add=""" <form action="#" method=post><dl><dt>{}:<dd><input type=text name={}><dt>{}:<dd><input type=text name={}><dd><input type=submit value=提交></dl></form>"""

    show=""" <form action="#" method=post><dl><dt>{}:<dd><input type=text name={}><dd><input type=submit value=提交></dl></form>"""
    out=""" <form action="#" method=post><dl><dt>{}:<dd><input type=text name={}><dd><input type=submit value=提交></dl></form>"""
    addmoney=""" <form action="#" method=post><dl><dt>{}:<dd><input type=text name={}><dd><input type=submit value=提交></dl></form>"""
    buy=""" <form action="#" method=post><dl><dt>{}:<dd><input type=text name={}><dd><input type=submit value=提交></dl></form>"""


@app.route("/show", endpoint="show" ,methods=['GET','POST'])
def show_daili(myid=None):
    if request.method=='GET':
        f=""" <form action="#" method=post><dl><dt>myid:<dd><input type=text name=myid><dd><input type=submit value=提交></dl></form>"""
        return f
    elif request.method=='POST':
        myid = request.form['myid']
        pass

    if myid==0: return "公司"
    self = dls_info_DB.query.filter_by(id=int(myid)).first()

    a = "名字：{}充值：{}货款：{}等级：{}折扣：{}上级：{}下级：{}下级总货款：{}待收利润：{}总计销售：{}已收利润：{}已提利润：{}".format(self.name, self.qian,
                                                                                         self.huokuan, self.dengji,
                                                                                         self.zk, self.updl,
                                                                                         self.downdl,
                                                                                         self.downdl_huokuan,
                                                                                         self.downdl_dslirun,
                                                                                         self.downdl_huikuan,
                                                                                         self.downdl_yslirun,
                                                                                         self.downdl_txlirun)

    return a

@app.route("/add", endpoint="add",methods=['GET','POST'])
def add_daili(name=None,updlid=None ):
    if request.method == 'GET':
        add = """ <form action="#" method=post><dl><dt>用户姓名name:<dd><input type=text name=name><dt>他的上级id公司为0 updlid:<dd><input type=text name=updlid><dd><input type=submit value=提交></dl></form>"""
        return add
    elif request.method == 'POST':
        name=request.form['name']
        updlid=request.form['updlid']
        pass
    else:
        name="小王"
        updlid=0

    dbs=dls_info_DB()
    dbs.name=name
    dbs.updl=updlid
    db.session.add(dbs)
    db.session.commit()

    #代理名字
    #上级代理  当前登陆用户作为上级代理
    #下级代理
    # dbs = src_DB.query.filter_by(content=None).all()
    return "add success  <a href='{}'>返回</a>".format(url_for('index'))
    pass

@app.route("/out", endpoint="out",methods=['GET','POST'])
def tui_daili(selfid=None):

    if request.method == 'GET':
        out = """ <form action="#" method=post><dl><dt>退出的id selfid:<dd><input type=text name=selfid><dd><input type=submit value=提交></dl></form>"""
        return out
    elif request.method == 'POST':
        selfid=request.form['selfid']
        pass
    else:
        selfid=0

    if selfid==0: return "公司？？退?"
    dbs1 = dls_info_DB.query.filter_by(id=int(selfid)).first()
    tui_dl_qian =dbs1.huokuan * dbs1.zk #退的代理折算的费用  #交接下级代理
    tui_zongzhang = tui_dl_qian + dbs1.downdl_yslirun - dbs1.downdl_txlirun #退代理总退钱
    tui_huokuan=dbs1.huokuan


    #安排 下级代理交接 接收退代理用户的下级代理

    db.session.commit()
    # 如果上级不是公司
    #安排 逐个级别退代收利润
    x_up_id = dbs1.updl
    x_up_zk = dbs1.zk
    x=0
    while 1:
        x=x+1
        print(x)
        #逐级退待收利润
        if int(x_up_id)>0:
            print(x_up_id)
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            lrhk = (tui_dl_qian / dbs.zk - tui_dl_qian / x_up_zk)  # 上级代理折扣-现在代理折扣等于代理折扣利润  代理商货款利润
            dbs.downdl_huokuan = float('%.2f' % float(dbs.downdl_huokuan - tui_huokuan))  # 总计下级代理结余货款 退代理的手上的货款  代理商货款
            dbs.downdl_dslirun = float('%.2f' % float(dbs.downdl_dslirun - lrhk * dbs.zk )) # 待收利润  剩余利润
            print("1---")
            db.session.commit()
            print("2---")

            x_up_id = dbs.updl
            x_up_zk = dbs.zk
            print(dbs.zk)
            print(dbs.updl)
        else:
            print("out")
            # 到公司，退出
            break
    # 下级代理标记交接
    print("标记代理")
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    if int(dbs.updl) > 0:
        dbs2 = dls_info_DB.query.filter_by(id=int(dbs.updl)).first()
        if dbs2:
            #下级代理待收货款利润交接
            dbs2.downdl_dslirun = dbs2.downdl_dslirun + dbs.downdl_dslirun  # 接收下级代理的待收利润
            dbs.downdl_dslirun=0
            # dbs.x_up_downdl_huokuan = dbs.downdl_huokuan + x_up_downdl_huokuan  # 接收下级代理的待收货款  +下级的货款已经算过了
            to_updl=dbs2.updl

            dbs.downdl_huokuan = 0
            dbs.downdl_dslirun = 0
            dbs.huokuan=0
            # 下级代理交接 修改上级代理
            dbs3 = dls_info_DB.query.filter_by(updl=int(dbs.id)).all()
            if dbs3:
                for i in dbs3:
                    print(i.id,i.name,i.updl)
                    i.updl=dbs2.id
            db.session.commit()
    check_daili_power(selfid)
    return "success : 去除已经提现的 可提现 {}<a href='{}'>返回</a>".format(tui_zongzhang,url_for('index'))

@app.route("/addmoney", endpoint="addmoney",methods=['GET','POST'])
def daili_chongqian(selfid=None,chongqian=None):

    if request.method == 'GET':
        addm = """ <form action="#" method=post><dl><dt>充值的id selfid:<dd><input type=text name=selfid><dt>充值金额 chongqian:<dd><input type=text name=chongqian><dd><input type=submit value=提交></dl></form>"""
        return addm
    elif request.method == 'POST':
        selfid=int(request.form['selfid'])
        chongqian=float(request.form['chongqian'])
        pass
    else:
        selfid=0
        chongqian=100
    # 代理级别（折扣）=代理规则（钱）
    pingguzhekou=""
    # 安排折扣
    if selfid == 0: return "公司"
    check_daili_power(selfid,chongqian)
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    dbs.qian = float(dbs.qian) + float(chongqian)
    dbs.huokuan = dbs.huokuan +chongqian / dbs.zk
    addhuokuan=dbs.huokuan
    #安排
    while 1:
        x_up_id=dbs.updl
        x_up_zk=dbs.zk
        db.session.commit()
        #利润安排
        if int(x_up_id)>0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            #安排代理商应收货款
            lr=(float(chongqian)/dbs.zk-float(chongqian)/x_up_zk) #上级代理折扣-现在代理折扣等于代理折扣利润
            if lr>0:
                dbs.downdl_huokuan=dbs.downdl_huokuan+addhuokuan # 总计下级代理结余货款 发展的下线手上的货款
                dbs.downdl_dslirun=dbs.downdl_dslirun+lr*dbs.zk# 待收利润
        else:
            break
    return "代理充钱分配完毕 <a href='{}'>返回</a>".format(url_for('index'))


@app.route("/buy", endpoint="buy",methods=['GET','POST'])
def buy(selfid=None,buy_pp=None):
    if request.method == 'GET':
        out = """ <form action="#" method=post><dl><dt>自己的id selfid:<dd><input type=text name=selfid><dt>消费金额 buy_pp:<dd><input type=text name=buy_pp><dd><input type=submit value=提交></dl></form>"""
        return out
    elif request.method == 'POST':
        selfid=request.form['selfid']
        buy_pp=float(request.form['buy_pp'])
        pass
    else:
        selfid=0
        buy_pp=1000
    if selfid == 0: return "公司"
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    if dbs.huokuan<buy_pp:return "钱不够。。。"

    dbs.huokuan=float(dbs.huokuan)-float(buy_pp)
    # 安排返利
    while 1:
        x_up_id = dbs.updl
        x_up_zk = dbs.zk
        db.session.commit()
        # 利润安排
        if int(x_up_id) > 0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            fq =  float(buy_pp )* float(x_up_zk)-float(buy_pp) * float(dbs.zk) #每个级别利润差
            if fq>0:
                dbs.downdl_huokuan = float(dbs.downdl_huokuan) - float(buy_pp)  # 总计下级代理结余货款 发展的下线手上的货款
                dbs.downdl_dslirun = dbs.downdl_dslirun - float(fq)  # 待收利润
                dbs.downdl_huikuan=dbs.downdl_huikuan+float(buy_pp) #已经卖了多少钱货
                dbs.downdl_yslirun = dbs.downdl_yslirun +float(fq)  # 已收利润
        else:
            #
            break
    pass
    return "buy success 购买完成 <a href='{}'>返回</a>".format(url_for('index'))

def look(self):
    a = "id：{}名字：{}充值：{}货款：{}等级：{}折扣：{}上级：{}下级：{}下级总货款：{}待收利润：{}总计销售：{}已收利润：{}已提走利润：{}".format(self.id,self.name, self.qian,
                                                                                         self.huokuan, self.dengji,
                                                                                         self.zk, self.updl,
                                                                                         self.downdl,
                                                                                         self.downdl_huokuan,
                                                                                         self.downdl_dslirun,
                                                                                         self.downdl_huikuan,
                                                                                         self.downdl_yslirun,
                                                                                         self.downdl_txlirun)

    return a

def check_down_guanxi():
    pass


def check_daili_power(id ,addmoney=0):
    self = dls_info_DB.query.filter_by(id=int(id)).first()
    qian=float(self.qian)+float(addmoney)
    if 600000 <=qian:
        self.dengji = 0
        self.zk = 0.25
    if 90000 <=qian < 600000:
        self.dengji = 1
        self.zk = 0.35
    if 30000 <= qian < 90000:
        self.dengji = 2
        self.zk = 0.5
    if 10000 <=qian < 30000:
        self.dengji = 3
        self.zk = 0.7
    db.session.commit()

if __name__ == "__main__":
    pass
    # get_content_to_db()
    app.run(debug=True,host="0.0.0.0",port=81)
    # app.run(debug=False)
