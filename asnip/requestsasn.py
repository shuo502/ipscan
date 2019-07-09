__author__ = 'yo'
# class as_info_DB(db.Model):
#     __tablename__ = 'asinfodb'
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     asnid=db.Column(db.String(512), nullable=True, comment="")
#     src=db.Column(db.Text, nullable=True, comment="")
#     companyname=db.Column(db.String(512), nullable=True, comment="")
#     country=db.Column(db.String(512), nullable=True, comment="")
#     url==db.Column(db.String(512), nullable=True, comment="")
#     uptime=db.Column(db.DateTime, index=True, default=datetime.now)
#     __table_args__ = {
#         "mysql_charset": "utf8"
#     }
class Session:

    token = ''
    cookies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    print("token:{}\ncookie:{}\nheaders:{}".format(token,cookies,headers))

#定义一个类，然后把类方法变成属性调用
class BaseResp:
    def __init__(self, sjson):
        self.data = json.loads(sjson)
        self.base_resp = self.data['base_resp']

    @property#方法变成属性调用
    def ret(self):
        return self.base_resp['ret']

class FakesResp(BaseResp): #继承 实现一个 超类
    def __init__(self, sjson):
        super(FakesResp, self).__init__(sjson)
        self.list = self.data['list']
        self.total = self.data['total']

    @property
    def count(self):
        return len(self.list)

def set_cookies( cookies):
# def set_cookies(driver, cookies):
    '''设置 浏览器 cookie'''
    Session.cookies = {}
    for item in cookies:
        # driver.add_cookie(item)
        Session.cookies[item['name']] = item['value']
    print('session.cookie: ' ,Session.cookies)

import  requests,json,os
cookies = json.load(open('cookies.json', 'rb')) if os.path.isfile('cookies.json') else []
url="https://bgp.he.net/AS174"
set_cookies(cookies)
g=requests.get(url,headers=Session.headers).content.decode()
print(g)