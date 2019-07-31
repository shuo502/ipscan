# conding=utf-8
import os
from datetime import timedelta, datetime
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import time
from decimal import *
import requests, re

# {"user":"root","passwd":"abcdefg","host":"2211.cc","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}
try:
    key = json.loads(open('key.json', 'r', encoding='utf-8').read())
except:
    s = '{"user":"user","passwd":"password","host":"host","port":"3306","dbname":"t7","charset":"utf8","secret_key":"abcdefghijklmn"}'
    open('key.json', 'w', encoding='utf-8').write(s)
    # print("编辑key.json")
    exit()
basedir = os.path.abspath(os.path.dirname(__file__))
mysql_config = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(key['user'], key['passwd'], key['host'], key['port'], key['dbname'], key['charset'])
# mysql_cuk = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(key['user'], key['passwd'], key['host'], key['port'],'tcuk_w7', key['charset'])
mysql_cuk ="mysql+pymysql://root:{}@{}:3306/{}?charset=utf8mb4".format(key['otherdb_passwd'],key['otherdb_host'],key['otherdb_dbname'])

sqlite_config = 'sqlite:///' + os.path.join(basedir, 'app.db')


# print(mysql_config)
class Config(object):
    # SECRET_KEY=key['secret_key']+str(os.urandom(24))
    SECRET_KEY = key['secret_key']
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)

    #配置同时连接多数据库
    SQLALCHEMY_BINDS = {
        'dls':mysql_config,
        'tcuk_w7':mysql_cuk
    }

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 默认数据库引擎
    # app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #
    # 设置session的保存时间。
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   sqlite_config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or mysql_config #连接默认数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


time.sleep(3)
static = './static'
template_folder = './templates'
app = Flask(__name__, static_folder=static, template_folder=template_folder, )
app.config.from_object(Config)
base_path_dir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)

# class hj_share_DB(db.Model):
#     __bind_key__ = 'tcuk_w7'
#     __tablename__ = 'hjmall_share'
#     # 代理商信息
#     '''
#     id
#     user_id
#     mobile
#     name
#     status
#     id_delete
#     addtime
#
#     '''

# class hj_order_detail_DB(db.Model):
#     __bind_key__ = 'tcuk_w7'
#     __tablename__ = 'hjmall_order_detail'
# #     订单明细
#     '''
#     id
#     order_id
#     goods_id
#     num
#     total_price
#     addtime
#     is_delete
#
#     '''

class hj_order_DB(db.Model):
    __bind_key__ = 'tcuk_w7'
    __tablename__ = 'hjmall_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id=db.Column(db.Integer, default=0, comment="")
    order_no=db.Column(db.String(255), nullable=True, comment="")
    total_price=db.Column(db.DECIMAL(10, 2),  comment="")
    pay_price=db.Column(db.DECIMAL(10, 2),  comment="")
    express_price=db.Column(db.DECIMAL(10, 2),  comment="")
    name=db.Column(db.String(255), nullable=True, comment="")
    mobile=db.Column(db.String(255), nullable=True, comment="")
    address=db.Column(db.String(255), nullable=True, comment="")
    remark=db.Column(db.String(255), nullable=True, comment="")
    is_pay=db.Column(db.Integer, default=0, comment="")
    pay_type=db.Column(db.Integer, default=0, comment="")
    is_send=db.Column(db.Integer, default=0, comment="")
    send_time=db.Column(db.Integer, default=0, comment="")
    is_confirm=db.Column(db.Integer, default=0, comment="")
    confirm_time=db.Column(db.Integer, default=0, comment="")
    apply_delete=db.Column(db.Integer, default=0, comment="")
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }

class hj_user_DB(db.Model):
    __bind_key__ = 'tcuk_w7'
    __tablename__ = 'hjmall_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(255), nullable=True, comment="")
    is_delete=db.Column(db.Integer, default=0, comment="")
    wechat_open_id=db.Column(db.String(255), nullable=True, comment="")
    nickname=db.Column(db.String(255), nullable=True, comment="")
    is_distributor=db.Column(db.Integer, default=0, comment="")
    parent_id=db.Column(db.Integer, default=0, comment="")
    parent_user_id=db.Column(db.Integer, default=0, comment="")
    time=db.Column(db.Integer, default=0, comment="")
    level=db.Column(db.Integer, default=0, comment="")
    money=db.Column(db.DECIMAL(10, 2),  comment="")
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }




class dls_info_DB(db.Model):
    __bind_key__ = 'dls'
    __tablename__ = 'dlsinfodb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True, comment="")
    dengji = db.Column(db.String(255), nullable=True, comment="")
    zk = db.Column(db.Float, default=1.0, comment="")
    qian = db.Column(db.Float, default=0, comment="")
    huokuan = db.Column(db.Float, default=0, comment="")
    updl = db.Column(db.Integer, default=0, comment="")
    selfbuy=db.Column(db.Float, default=0, comment="自己卖货")
    downdl = db.Column(db.String(4096), nullable=True, comment="")
    downdl_huokuan = db.Column(db.Float, default=0, comment="总计下级代理结余货款 发展的下线手上的货款")
    downdl_dslirun = db.Column(db.Float, default=0, comment="待收利润")
    downdl_huikuan = db.Column(db.Float, default=0, comment="总计下级代理销售")
    downdl_yslirun = db.Column(db.Float, default=0, comment="已收利润")
    downdl_txlirun = db.Column(db.Float, default=0, comment="提现利润")
    uptime = db.Column(db.DateTime, index=True, default=datetime.now)
    addname = db.Column(db.String(255), nullable=True, comment="")
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    status = db.Column(db.String(255), nullable=True, comment="")
    __table_args__ = {
        "mysql_charset": "utf8"
    }


class dls_log_DB(db.Model):
    __bind_key__ = 'dls'
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
    o = look_dls()
    nav = """<br>
    <a href="{}">查看结算信息<a><br>
    <a href="{}">查看代理商信息<a><br>
    <a href="{}">增加代理<a><br>
    <a href="{}">退出代理<a><br>
    <a href="{}">增加钱<a><br>
    <a href="{}">购买<a><br>
    <a href="{}">提现<a><br>
    <br><br><a href="{}">清空<a><br><br>
    """.format( url_for('exttab'),url_for('show'), url_for('add'), url_for('out'), url_for('addmoney'), url_for('buy'), url_for('tixian'),
               url_for('removes'))
    dbs = dls_info_DB.query.filter_by().all()
    allus = ""
    hk = 0
    qian = 0
    shengyu = 0
    yt = 0
    if dbs:
        for i in dbs:
            b = look(i)
            qian = qian + i.qian
            shengyu = shengyu + i.downdl_yslirun
            yt = yt + i.downdl_txlirun
            if i.updl == 0 or i.updl == None:
                hk = (float(i.downdl_huikuan) + float(hk)) * 0.25
            allus = allus + "{} <br>".format(b)
    else:
        allus = "还没有代理商"
    qian = qian - yt
    shengyu = shengyu - yt
    z = qian - hk
    x = """<br>账户{}个,总剩余资金池{},已经分配待支付资金池{},支付已提现资金{},<br>公司销售 需要扣除 成本:{} 扣除后资金池剩余:{}<br>""".format(len(dbs), qian, shengyu,
                                                                                               yt, hk, z)
    return nav+o+x + allus


def look_dls():
    dbs = dls_info_DB.query.filter_by().all()
    s = "id：0  |公司 ||"
    for i in dbs:
        s = s + "id:{} |名字:{} ||".format(i.id, i.name)
    return s




@app.route("/removes", endpoint="removes", methods=['GET', 'POST'])
def removes():
    all = dls_info_DB.query.filter_by().all()
    for i in all:
        o = dls_info_DB.query.filter_by(id=int(i.id)).first()
        if o:
            #     print(o)
            #     print(o.id)
            #     print(o.name)
            #     db.session.remove()
            db.session.delete(o)
            db.session.commit()

    return "已删除所有用户"


@app.route("/show", endpoint="show", methods=['GET', 'POST'])
def show_daili(myid=None):
    if request.method == 'GET':
        o = look_dls()
        f = """<br> <form action="#" method=post><dl><dt>myid:<dd><input type=text name=myid><dd><input type=submit value=提交></dl></form>"""
        return o + f
    elif request.method == 'POST':
        myid = request.form['myid']
        pass

    if myid == 0: return "公司"
    self = dls_info_DB.query.filter_by(id=int(myid)).first()

    a = "<br>名字：{}充值：{}货款：{}等级：{}折扣：{}上级：{}下级：{}下级总货款：{}待收利润：{}总计销售：{}已收利润：{}已提利润：{}<br>".format(self.name, self.qian,
                                                                                         self.huokuan, self.dengji,
                                                                                         self.zk, self.updl,
                                                                                         self.downdl,
                                                                                         self.downdl_huokuan,
                                                                                         self.downdl_dslirun,
                                                                                         self.downdl_huikuan,
                                                                                         self.downdl_yslirun,
                                                                                         self.downdl_txlirun)
    infos=dls_log_DB.query.filter_by(user=str(myid)).all()
    r="<br>"
    for i in infos:
       r=r+"{}：[{}]id:{}---{}<br>".format(i.id,i.sometime,i.user,i.something)

    return a+r


@app.route("/add", endpoint="add", methods=['GET', 'POST'])
def add_daili(name=None, updlid=None):
    if request.method == 'GET':
        o = look_dls()
        add = """<br> <form action="#" method=post><dl><dt>用户姓名name:<dd><input type=text name=name><dt>他的上级id公司为0 updlid:<dd><input type=text name=updlid><dd><input type=submit value=提交></dl></form>"""
        return o + add
    elif request.method == 'POST':
        name = request.form['name']
        updlid = request.form['updlid']
        pass
    else:
        name = "小王"
        updlid = 0
    dbs = dls_info_DB()
    dbs.name = name
    dbs.updl = updlid
    db.session.add(dbs)

    db.session.commit()
    logs=dls_log_DB()
    logs.user=dbs.id
    logs.something="上级{},发展的代理商{},".format(name,updlid)
    db.session.add(logs)
    # 代理名字
    # 上级代理  当前登陆用户作为上级代理
    # 下级代理
    # dbs = src_DB.query.filter_by(content=None).all()
    return "add success  <a href='{}'>返回</a>".format(url_for('index'))
    pass


@app.route("/out", endpoint="out", methods=['GET', 'POST'])
def tui_daili(selfid=None, updl_is_h=None):

    if request.method == 'GET':
        tps = "<br>公司不能直接接管下级发展的代理。否则利润不计算，需要增加一个总代接收。<br>"
        o = look_dls()
        out = """<br> <form action="#" method=post><dl><dt>退出的id selfid:<dd><input type=text name=selfid><dt>指定上级的接收下级代理的id（不指定默认为上级接收）:<dd><input type=text name=updl_is_h><dd><input type=submit value=提交></dl></form>"""
        return tps + o + out
    elif request.method == 'POST':
        selfid = request.form['selfid']
        updl_is_h = request.form['updl_is_h']
        pass
    else:
        selfid = 0
        updl_is_h = None

    if selfid == 0: return "公司？？退?"


    dbs1 = dls_info_DB.query.filter_by(id=int(selfid)).first()
    tui_dl_qian = dbs1.huokuan * dbs1.zk  # 退的代理折算的费用  #交接下级代理
    tui_zongzhang = tui_dl_qian + dbs1.downdl_yslirun - dbs1.downdl_txlirun  # 退代理总退钱
    tui_huokuan = dbs1.huokuan

    logs = dls_log_DB()
    logs.something = "退代理商[id{}:{}]".format(dbs1.id,dbs1.name)
    db.session.add(logs)

    db.session.commit()
    # 如果上级不是公司
    # 安排 逐个级别退代收利润
    x_up_id = dbs1.updl
    x_up_zk = dbs1.zk
    x = 0
    while 1:
        x = x + 1
        # print(x)
        # 逐级退待收利润
        if int(x_up_id) > 0:
            # print(x_up_id)
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            lrhk = (tui_dl_qian / dbs.zk - tui_dl_qian / x_up_zk)  # 上级代理折扣-现在代理折扣等于代理折扣利润  代理商货款利润
            dbs.downdl_huokuan = float('%.2f' % float(dbs.downdl_huokuan - tui_huokuan))  # 总计下级代理结余货款 退代理的手上的货款  代理商货款
            dbs.downdl_dslirun = float('%.2f' % float(dbs.downdl_dslirun - lrhk * dbs.zk))  # 待收利润  剩余利润
            # print("1---")

            logs = dls_log_DB()
            logs.something = "[id{}:{}]退代理商,[id{}:{}]作为上级扣除自己账户下级退代理货款后{}，扣除自己代收利润后{}".format(dbs1.id, dbs1.name,dbs.id,dbs.name,dbs.downdl_huokuan,dbs.downdl_dslirun)
            db.session.add(logs)

            db.session.commit()
            # print("2---")

            x_up_id = dbs.updl
            x_up_zk = dbs.zk
            # print(dbs.zk)
            # print(dbs.updl)


        else:
            # print("out")
            # 到公司，退出
            break
    # 安排 下级代理交接 接收退代理用户的下级代理
    # 下级代理标记交接
    # print("标记代理")
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    if updl_is_h:
        updl = updl_is_h
        pass
    else:
        updl = dbs.updl
    if int(updl) > 0:
        dbs2 = dls_info_DB.query.filter_by(id=int(updl)).first()
        if dbs2:
            # 下级代理待收货款利润交接
            dbs2.downdl_dslirun = dbs2.downdl_dslirun + dbs.downdl_dslirun  # 接收下级代理的待收利润
            # dbs.x_up_downdl_huokuan = dbs.downdl_huokuan + x_up_downdl_huokuan  # 接收下级代理的待收货款  +下级的货款已经算过了
            to_updl = dbs2.updl

            logs = dls_log_DB()
            logs.user = dbs2.id
            logs.something = "[id{}:{}]接收[id{}{}]的代理商代利润后{}".format(dbs2.id, dbs2.name,dbs.id,dbs.name,
                                                                                        dbs2.downdl_yslirun)
            db.session.add(logs)
            db.session.commit()

            dbs.downdl_dslirun = 0
            dbs.downdl_huokuan = 0
            dbs.huokuan = 0
            dbs.downdl_yslirun = tui_zongzhang
            logs = dls_log_DB()
            logs.user = dbs.id
            logs.something = "[id{}:{}]清空账户下级代理商代收利润账户,清空账户下级代理商代收货款账户,更新总可提现利润账户{}".format(dbs.id,dbs.name,dbs.downdl_yslirun)
            db.session.add(logs)
            db.session.commit()
            # 下级代理交接 修改上级代理
            dbs3 = dls_info_DB.query.filter_by(updl=int(dbs.id)).all()
            if dbs3:
                for i in dbs3:
                    logs = dls_log_DB()
                    logs.user = dbs3.id
                    logs.something = "修改[id{}:{}]的下级代理[id{}]的上级代理为[id{}:{}]".format(dbs.id, dbs.name, dbs.updl,dbs3.id,dbs3.name)
                    db.session.add(logs)
                    # print(i.id, i.name, i.updl)
                    i.updl = to_updl
                    db.session.commit()

    check_daili_power(selfid)
    return "success : 去除已经提现的 可提现 {}<a href='{}'>返回</a>".format(tui_zongzhang, url_for('index'))


@app.route("/tixian", endpoint="tixian", methods=['GET', 'POST'])
def tixian(selfid=None, tiqian=None):
    o = look_dls()
    if request.method == 'GET':
        addm = """<br> <form action="#" method=post><dl><dt>提现的id selfid:<dd><input type=text name=selfid><dt>提现金额 tiqian:<dd><input type=text name=tiqian><dd><input type=submit value=提交></dl></form>"""
        return o + addm
    elif request.method == 'POST':
        selfid = int(request.form['selfid'])
        tiqian = float(request.form['tiqian'])
        pass
    else:
        selfid = 0
        tiqian = 100
    if selfid == 0: return "公司"
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    if float(tiqian) > float(dbs.downdl_yslirun): return "钱不够啊" # 对比
    dbs.downdl_yslirun = float(dbs.downdl_yslirun) - float(tiqian)
    dbs.downdl_txlirun = float(dbs.downdl_txlirun) + float(tiqian)
    logs = dls_log_DB()
    logs.user = dbs.id
    logs.something = "[id{}:{}]提现{} ,剩余可提现{},已经提现{}".format(dbs.id, dbs.name,tiqian,dbs.downdl_yslirun,dbs.downdl_txlirun)
    db.session.add(logs)
    db.session.commit()
    return "已经完成提现操作"


@app.route("/addmoney", endpoint="addmoney", methods=['GET', 'POST'])
def daili_chongqian(selfid=None, chongqian=None):
    o = look_dls()
    if request.method == 'GET':
        addm = """<br> <form action="#" method=post><dl><dt>充值的id selfid:<dd><input type=text name=selfid><dt>充值金额 chongqian:<dd><input type=text name=chongqian><dd><input type=submit value=提交></dl></form>"""
        return o + addm
    elif request.method == 'POST':
        selfid = int(request.form['selfid'])
        chongqian = float(request.form['chongqian'])
        pass
    else:
        selfid = 0
        chongqian = 100
    # 代理级别（折扣）=代理规则（钱）
    pingguzhekou = ""
    # 安排折扣
    if selfid == 0: return "公司"
    check_daili_power(selfid, chongqian)
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    dbs.qian = float(dbs.qian) + float(chongqian)
    dbs.huokuan = dbs.huokuan + chongqian / dbs.zk
    addhuokuan = dbs.huokuan
    logs = dls_log_DB()
    logs.user = dbs.id
    logs.something = "[id{}:{}]充值{} 折扣{} 累计货款{}".format(dbs.id, dbs.name, chongqian, dbs.zk,addhuokuan)
    selfname=dbs.name

    db.session.add(logs)

    # 安排
    while 1:
        x_up_id = dbs.updl
        x_up_zk = dbs.zk
        db.session.commit()
        # 利润安排
        if int(x_up_id) > 0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            # 安排代理商应收货款
            lr = (float(chongqian) / dbs.zk - float(chongqian) / x_up_zk)  # 上级代理折扣-现在代理折扣等于代理折扣利润
            if lr > 0:
                dbs.downdl_huokuan = dbs.downdl_huokuan + addhuokuan  # 总计下级代理结余货款 发展的下线手上的货款
                dbs.downdl_dslirun = dbs.downdl_dslirun + lr * dbs.zk  # 待收利润
            logs = dls_log_DB()
            logs.user=dbs.id
            logs.something = "[id{}:{}]充值 上级代理[id{}:{}]增加下级代理商账户货款后{}，增加下级代理商利润{}".format(selfid,selfname,dbs.id,dbs.name,dbs.downdl_huokuan,dbs.downdl_dslirun)
            db.session.add(logs)
        else:
            break
    return "代理充钱分配完毕 <a href='{}'>返回</a>".format(url_for('index'))


@app.route("/buy", endpoint="buy", methods=['GET', 'POST'])
def buy(selfid=None, buy_pp=None):
    if request.method == 'GET':
        o = look_dls()
        out = """<br> <form action="#" method=post><dl><dt>自己的id selfid:<dd><input type=text name=selfid><dt>消费金额 buy_pp:<dd><input type=text name=buy_pp><dd><input type=submit value=提交></dl></form>"""
        return o + out
    elif request.method == 'POST':
        selfid = request.form['selfid']
        buy_pp = float(request.form['buy_pp'])
        pass
    else:
        selfid = 0
        buy_pp = 1000
    if selfid == 0: return "公司"
    dbs = dls_info_DB.query.filter_by(id=int(selfid)).first()
    # if dbs.huokuan < buy_pp: return "钱不够。。。"#对比
    dbs.selfbuy=dbs.selfbuy+buy_pp
    dbs.huokuan = float(dbs.huokuan) - float(buy_pp)
    selfname=dbs.name
    logs = dls_log_DB()
    logs.user = dbs.id
    logs.something = "[id{}:{}] 扣货款{} 剩余货款{},账户总计扣{}".format(dbs.id, dbs.name,buy_pp,dbs.huokuan,dbs.selfbuy)
    db.session.add(logs)
    db.session.commit()


    # 安排返利
    while 1:
        x_up_id = dbs.updl
        x_up_zk = dbs.zk
        db.session.commit()
        # 利润安排
        if int(x_up_id) > 0:
            dbs = dls_info_DB.query.filter_by(id=int(x_up_id)).first()
            fq = float(buy_pp) * float(x_up_zk) - float(buy_pp) * float(dbs.zk)  # 每个级别利润差
            if fq > 0:
                dbs.downdl_huokuan = float(dbs.downdl_huokuan) - float(buy_pp)  # 总计下级代理结余货款 发展的下线手上的货款
                dbs.downdl_dslirun = dbs.downdl_dslirun - float(fq)  # 待收利润
                dbs.downdl_huikuan = dbs.downdl_huikuan + float(buy_pp)  # 已经卖了多少钱货
                dbs.downdl_yslirun = dbs.downdl_yslirun + float(fq)  # 已收利润
            logs = dls_log_DB()
            logs.user = dbs.id
            logs.something = "[id{}:{}]销售扣货款{},上级代理[id{}:{}]代理账户扣下级代理销售货款后{},本单获得佣金{},".format(selfid,selfname, buy_pp,dbs.id, dbs.name,dbs.downdl_huokuan,fq)
            db.session.add(logs)
            db.session.commit()
        else:
            #
            break
    pass
    return "buy success 购买完成 <a href='{}'>返回</a>".format(url_for('index'))


def look(self,upname=None):
    if upname:self.updl=str(upname)+" id:"+str( self.updl)
    a = "id：{} |名字：{} |充值：{} |货款：{} |等级：{} |折扣：{} |上级ID：{} |下级(还未写入)：{} |下级总货款：{} |待收利润：{} |总计销售：{} |已收利润：{} |已提走利润：{}".format(
        self.id, self.name, self.qian,
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


def check_daili_power(id, addmoney=0):
    self = dls_info_DB.query.filter_by(id=int(id)).first()
    qian = float(self.qian) + float(addmoney)
    if 600000 <= qian:
        self.dengji = 0
        self.zk = 0.25
    if 90000 <= qian < 600000:
        self.dengji = 1
        self.zk = 0.35
    if 30000 <= qian < 90000:
        self.dengji = 2
        self.zk = 0.5
    if 10000 <= qian < 30000:
        self.dengji = 3
        self.zk = 0.7
    logs = dls_log_DB()
    logs.something = "[id{}:{}]用户充值:{} 初始化折扣 {} 初始化等级{},".format(self.id,self.name,addmoney,self.zk,self.dengji )
    db.session.add(logs)
    db.session.commit()


@app.route("/exttab", endpoint="exttab", methods=['GET', 'POST'])
def exttab(selfid=None, buy_pp=None):
    dbs = dls_info_DB.query.filter_by().all()
    x=[]
    d={0:'公司'}
    hk=0
    for self in dbs:
       d[self.id]=self.name
    for  self in dbs:
        if self.updl==0:
            hk=self.downdl_huikuan+self.selfbuy+hk
        x.append([self.id,self.name,d[self.updl], float('%.2f' % float(self.huokuan*self.zk)),self.zk,self.downdl_yslirun,float('%.2f' % float(self.downdl_huikuan*self.zk)),self.selfbuy])
    hk=hk*0.25
    x.append([0,'公司',0,0,0,hk])
    # print(x)
    return render_template('suan.html',x=x)

    # self.huokuan, self.dengji,
    # self.zk, self.updl,
    # self.downdl,
    # self.downdl_huokuan,
    # self.downdl_dslirun,
    # self.downdl_huikuan,
    # self.downdl_yslirun,
    # self.downdl_txlirun
    #
    # yszk=self.huokuan*self.zk
    # yj=self.downdl_yslirun

    pass


# @app.route("/sells", endpoint="sells", methods=['GET', 'POST'])
# def sells(selfid=None, buy_pp=None):
#     if request.method == 'GET':
#         o = look_dls()
#         out = """<br> <form action="#" method=post><dl><dt>自己的id selfid:<dd><input type=text name=selfid><dt>消费金额 buy_pp:<dd><input type=text name=buy_pp><dd><input type=submit value=提交></dl></form>"""
#         return o + out
#     elif request.method == 'POST':
#         selfid = request.form['selfid']
#         buy_pp = float(request.form['buy_pp'])
#         pass
#     else:
#         selfid = 0
#         buy_pp = 1000
#
#     pass
#     return ""

@app.route("/change_zk", endpoint="change_zk", methods=['GET', 'POST'])
def change_zk(selfid=None, zk=None):
    if request.method == 'GET':
        o = look_dls()
        out = """<br> <form action="#" method=post><dl><dt>要修改的id selfid:<dd><input type=text name=selfid><dt>修改的折扣 小于1:<dd><input type=text name=zk><dd><input type=submit value=提交></dl></form>"""
        return o + out
    elif request.method == 'POST':
        selfid = request.form['selfid']
        zk = float(request.form['zk'])
        pass
    else:
        selfid = 0
        zk = 1
    self = dls_info_DB.query.filter_by(id=int(selfid)).first()
    if zk<=1:
        self.zk=float(zk)
        db.session.commit()
    pass
    return "success change zk"



@app.route("/change_gx", endpoint="change_gx", methods=['GET', 'POST'])
def change_gx(selfid=None, change_updl=None):
    if request.method == 'GET':
        o = look_dls()
        out = """<br> <form action="#" method=post><dl><dt>要修改的id selfid:<dd><input type=text name=selfid><dt>修改上级的id:<dd><input type=text name=change_updl><dd><input type=submit value=提交></dl></form>"""
        return o + out
    elif request.method == 'POST':
        selfid = request.form['selfid']
        change_updl = int(request.form['change_updl'])
        pass
    else:
        selfid = 0
        change_updl = 1

    self = dls_info_DB.query.filter_by(id=int(selfid)).first()
    # 检查代理关系
    err=1
    dbs=self
    while 1:
        if dbs.updl==int(selfid):
            err=0
            break
        if dbs.updl == 0:
            break
        dbs=dls_info_DB.query.filter_by(id=int(self.updl)).first()

    if err:
        self.updl=int(change_updl)
        db.session.commit()
    else:
        return "err"

    # 我的上级有没有我的下级。
    # 获取上级
    # 获取下级
    #如果我的上级有我
    # 出错

    return "success"

@app.route("/get_gx", endpoint="get_gx", methods=['GET', 'POST'])
def get_gx():
    dbs=hj_user_DB.query.filter_by().all()
    global user_dict
    user_dict={}#防止历史数据出错
    # i.level
    zk_dict={
        '-1': 1,
        '0': 1,
        '4':2.5,
        '3':3.5,
        '2':5,
        '1':7,
    }
    for i in dbs:
        if i.is_delete==0:
            print(i.level)
            zk=zk_dict[str(i.level)]
            # user_dict[i.id]={'id':i.id,'username':i.username,'open_id':i.wechat_open_id,'nickname':i.nickname,'is_distributor':i.is_distributor,'parent_id':i.parent_id,'parent_user_id':i.parent_user_id,'time':i.time,'level':i.level,'money':i.money,'zk':zk}
            user_dict[i.id]={'id':i.id,'nickname':i.nickname,'is_distributor':i.is_distributor,'parent_id':i.parent_id,'parent_user_id':i.parent_user_id,'time':i.time,'level':i.level,'money':i.money,'zk':zk}
            user_dict[i.id]['selfsell']=0
            user_dict[i.id]['downsell']=0
            user_dict[i.id]['yongjin']=0
            user_dict[i.id]['koumoney']=0
            user_dict[i.id]['fankuan']=0

    e={}
    for i in user_dict:

        if int(user_dict[i]['is_distributor']) !=1:
            pass
            # e[user_dict[i]['id']]['updl'] = "普通用户"
        else:
            e[user_dict[i]['id']] = user_dict[i]
            updl = user_dict[i]['parent_id']
            if updl>0:
                e[user_dict[i]['id']]['updl']=user_dict[updl]['nickname']
            else:
                e[user_dict[i]['id']]['updl']="总代"
    for x in e:
        i=e[x]
        # print(e[i])
        r="id:{} {} 上级代理{} {} 折扣等级{}  账户余额{}".format(i["id"],i["nickname"],i['parent_id'],i['updl'],i['level'],i['money'])
        print(r)
    return "r"

@app.route("/get_sell", endpoint="get_sell", methods=['GET', 'POST'])
def get_sell():
    get_gx()
    o=hj_order_DB.query.filter_by().all()
    global user_dict, user_dict_log
    change_user_dict=user_dict
    sell_dict={}
    for i in o:

        if int(i.is_confirm)==1: #收货
            if i.user_id not in sell_dict:sell_dict[i.user_id]=[]
            # print(i.confirm_time)#收货时间
            # print(user_dict[i.user_id]['nickname'])#下单用户
            # print(i.total_price)#销售
            # dates=time.strftime("%Y/%m/%d %H:%M:%S", i.confirm_time)
            #当天-开始时间  当天-结束时间。
            timeArray = time.localtime( i.confirm_time)

            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S" , timeArray)
            # str=timeArray = time.strptime(dates,  "%Y-%m-%d %H:%M:%S" )
            e="用户：{}{} 下单实收金额{} 原价{}下单时间{}".format(i.user_id,user_dict[i.user_id]['nickname'],i.pay_price,i.total_price,otherStyleTime)
            sell_dict[i.user_id].append(e)
            print(e)
            change_user_dict=sell_logic(change_user_dict,i.user_id,i.pay_price)

    user_dict=change_user_dict
    for i in user_dict:
        if int(user_dict[i]['is_distributor']) != 1:
            pass
        else:
            print(user_dict[i])
    # print(user_dict)
    for i in user_dict_log:
        print(user_dict_log[i])

    r=render_template('t.html',x=user_dict,sell_d=sell_dict,log_s=user_dict_log)

    return r


    # 提取销售数据
    #插入数据库 写入销售。计算
    #
    pass
@app.route("/set_null", endpoint="set_null", methods=['GET', 'POST'])
def set_null():

    # 清空
    #
    pass

"""
获取订单
还原折扣额
计算。

"""
def logic_logs(sellid,msg):
    t=time.time()
    global user_dict_log
    if sellid not in  user_dict_log:
        user_dict_log[sellid]=[]
    user_dict_log[sellid].append("{} - {}".format(t,msg))

def sell_logic(in_user_info,sellid,zksellpp):
    # 折扣还原成销售金额
    if len(in_user_info)<=0 or sellid<=0 or zksellpp<=0:
        return in_user_info
    user_info=in_user_info
    i_am=user_info[sellid]
    if "selfsell" not in  i_am:
        i_am['selfsell']=0
    sellpp= float('%.2f' % float(float(zksellpp)/float(i_am['zk'])*10))#还原原价
    i_am['selfsell'] = float(i_am['selfsell']) + float(sellpp)
    selfname = i_am['nickname']
    i_am['fankuan'] =i_am['selfsell']+i_am['downsell']+i_am['yongjin']
    i_am['koumoney'] = i_am['selfsell'] + i_am['downsell']
    logic_logs(i_am['id'],"[id{}:{}] 下单扣货款{} 货款{},本月总计下单货款{},销售反货款{}(需从货款中扣除),账户打钱{}".format(i_am['id'], i_am['nickname'], sellpp, i_am['money'], i_am['selfsell'],i_am['koumoney'],i_am['fankuan']))
    user_info[i_am['id']]=i_am
    new_p=i_am
    # 安排返利
    while 1:
        x_up_id = new_p['parent_id']
        x_up_zk = i_am['zk']
        db.session.commit()
        # 利润安排
        if int(x_up_id) > 0:
            new_p={}
            new_p=user_info[x_up_id]
            yj =  float('%.2f' % float(float(sellpp) * float(x_up_zk)/10 - float(sellpp) * float(new_p['zk'])/10 )) # 每个级别利润差
            new_p['downsell'] =  float('%.2f' % float(float(new_p['downsell']) +float(sellpp)))
            new_p['yongjin'] = float(new_p['yongjin'])+float(yj)
            new_p['fankuan'] =  float('%.2f' % float(new_p['selfsell'] + new_p['downsell'] + new_p['yongjin']))
            new_p['koumoney'] =  float('%.2f' % float(new_p['selfsell'] + new_p['downsell']))
            user_info[new_p['id']] = new_p
            logic_logs(new_p['id'],"[id{}:{}]折扣销售{},上级代理[id{}:{}],本单获得佣金{},代理账户获得返款{}".format(sellid, selfname,zksellpp , new_p['id'], new_p['nickname'], yj,sellpp))
        else:
            break

    return user_info


if __name__ == "__main__":
    user_dict={}
    user_dict_log={}
    pass
    # get_content_to_db()
    app.run(debug=True, host="192.168.0.147", port=5001)
    # app.run(debug=False)
