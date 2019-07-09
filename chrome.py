# -*- coding: utf-8 -*-
from selenium import webdriver
import time
# from bs4 import BeautifulSoup
import requests
import re
import shutil
import os
import json
import argparse
import traceback
import random
import math
import codecs

class Urls:
    ipipas='https://www.ipip.net/ip.html'
    ipas="https://whois.ipip.net/AS36352"
    # index='https://liveplatform.taobao.com/live/liveDetail.htm?spm=a1z9u.8142865.0.0.42f134edtcD30s&id=230205911611'
    # index = 'https://mp.weixin.qq.com'
    # editor = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token={token}'
    # query_biz = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={token}&lang=zh_CN&f=json&ajax=1&random={random}&query={query}&begin={begin}&count={count}'
    # query_arti = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&%E2%80%A65&action=list_ex&begin={begin}&count={count}&query={query}&fakeid={fakeid}&type=9'

#定义session
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

def set_cookies(driver, cookies):
    '''设置 浏览器 cookie'''
    Session.cookies = {}
    for item in cookies:
        driver.add_cookie(item)
        Session.cookies[item['name']] = item['value']
    print('session.cookie: ' ,Session.cookies)

def download(url, sname):
    '''打开 重试3次  调用session head 打开网页  写入文件  分块写入'''
    for i in range(0, 3):
        result = requests.get(url, headers=Session.headers, stream=True)
        if result.status_code == 200:
            with open(sname, 'wb') as f:
                for chunk in result.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            continue
    print("Error download:{url}")
    return False

# def verfy_arti_content(html):
#     if not html:
#         return False, "从服务器获取失败"
#     pat = re.compile(r'<div class="page_msg')
#     if not pat.search(html):
#         return True, ""
#     pat = re.compile(r'<div class="global_error_msg.*?">(.*?)</div', re.MULTILINE | re.DOTALL)
#     ms = pat.findall(html)
#     if ms:
#         return False, ms[0].strip()
#     return False, "服务器返回未知错误"
#
#
#
#  rep = requests.get(
#         Urls.query_arti.format(token=Session.token, fakeid=fakeid, begin=begin, count=pagesize, query=query),
#         cookies=Session.cookies, headers=Session.headers)
#
# rep = requests.get(url, cookies=Session.cookies, headers=Session.headers)


def main(chrome):
    # 会过期, 重新登录后需要重新取得 #浏览器登陆 ，然后获得cookies 然后用requests 处理
    if not chrome:

        if os.path.isfile('chromedriver'):
            chrome = 'chromedriver'
        else:
            chrome = input('输入webchrome:').strip()
    driver = webdriver.Chrome(executable_path=chrome)
    cookies = json.load(open('cookies.json', 'rb')) if os.path.isfile('cookies.json') else []
    driver.get(Urls.ipipas)
    if not cookies:
        input("请先手动登录, 完成后按回车继续:")
        cookies = driver.get_cookies()
        # cookies = {'thw': 'cn', ' cna': 'n2rIFFpPJH0CAXt1aEwGZ3WY', ' tg': '0', ' x': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0', ' hng': 'CN%7Czh-CN%7CCNY%7C156', ' UM_distinctid': '169276ffe86294-02f668bd8af519-58422116-1fa400-169276ffe892b4', ' miid': '960049641392677858', ' enc': 'lSUmox1Me%2BGZ1BxoGE%2BgegIjZdRACvQorjFufayiZ0BTKrnfL0d%2Bb83FoXAXZZdF%2F0zzoh%2FzKIPojxAQMQDNvg%3D%3D', ' t': '0e1adc5fe9cbf3030e43e83df57c40d6', ' cookie2': '5e90542bc00051017ee8974faeb95848', ' v': '0', ' _tb_token_': '3e13ee57e57be', ' unb': '4087646153', ' uc1': 'cookie16', ' sg': '%E5%BA%9732', ' _l_g_': 'Ug%3D%3D', ' skt': '8408cbc7525c09b7', ' cookie1': 'VqwS0EdjyC2q7gv4R3l9IY7LZoNrvUwijJPpvM9dFuA%3D', ' csg': '9ceb3ec6', ' uc3': 'vt3', ' existShop': 'MTU2MjA0Njk5Nw%3D%3D', ' tracknick': 'cuk%5Cu7F8E%5Cu5BB9%5Cu5DE5%5Cu5177%5Cu65D7%5Cu8230%5Cu5E97', ' lgc': 'cuk%5Cu7F8E%5Cu5BB9%5Cu5DE5%5Cu5177%5Cu65D7%5Cu8230%5Cu5E97', ' _cc_': 'VFC%2FuZ9ajQ%3D%3D', ' dnk': 'cuk%5Cu7F8E%5Cu5BB9%5Cu5DE5%5Cu5177%5Cu65D7%5Cu8230%5Cu5E97', ' _nk_': 'cuk%5Cu7F8E%5Cu5BB9%5Cu5DE5%5Cu5177%5Cu65D7%5Cu8230%5Cu5E97', ' cookie17': 'VyyZGEXCid08bg%3D%3D', ' mt': 'ci', ' _m_h5_tk': '62379c85c210e8ce975951a223c8d230_1562054919022', ' _m_h5_tk_enc': 'cece26c30ca3296baffaffc1f3b4ee6f', ' l': 'bBgegXHHvvMEVugMBOCZnurza779IIRAguPzaNbMi_5QM6L_t4QOkA-ppFp6Vj5R_ZYB4G2npwy9-etkm', ' isg': 'BFhY9iBdsSE4xJxHKqxvvKXPKYYq6bxYyFFr0pJJpxNGLfgXOlP5Ww8LZSW4PXSj'}

        open('cookies.json', 'wb').write(json.dumps(cookies).encode('utf-8'))

    set_cookies(driver, cookies)
    # driver.get(Urls.ipipas)
    url = driver.current_url
    # print(url)
    # y=driver.page_source
    # print(y)
    result = requests.get(url, headers=Session.headers)
    print(result.content)

    # if 'token' not in url:
    #     # raise Exception(f"获取网页失败!")
    #     cookies=input("请先手动登录, 完成后按回车继续:")
    #     cookies={i.split("=")[0]: i.split("=")[1] for i in cookies.split(';')}
    #     set_cookies(driver, cookies)
    #     driver.get(Urls.index)
    #     url = driver.current_url
    # Session.token = re.findall(r'token=(\w+)', url)[0]
chrome=None
# main(chrome)

cookies = json.load(open('cookies.json', 'rb')) if os.path.isfile('cookies.json') else []
if not cookies:
    main(chrome)
result = requests.get(Urls.ipas, headers=Session.headers)
print(result.content.decode())



# main('chromedriver')
# i='C:\\Users\\yo\\Desktop\\git\\yo\\zhibo\\chromedriver'
# print(os.path.isfile(i))
#
# if os.path.isfile('chromedriver'):
#     chrome = 'chromedriver'
#     print(chrome)