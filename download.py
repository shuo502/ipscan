import re,os
import requests

def check_path(url):
    f1=url.rfind("/")
    f2=url.find("//")
    files="./"+url[f2+2:f1]
    file=url[f1+1:]
    if os.path.isdir(files) == False:
        os.makedirs(files)
    pathfile=str(files)+"/"+str(file)
    if os.path.isfile(pathfile):
        print("file is save")
        pathfile=None
    return pathfile

import random
headers={
"Host": "www.vmgirls.com",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36  pa xiao shi le beifen yi xia baoqian "
}
def downloadfile(url):
    global x
    file=check_path(url)
    if file:
        time.sleep(0.5)

        if x==True:
            x=False
        else:
            x=True

        if x:
            url=url.replace("www","static")
            r = requests.get(url, headers=headers, timeout=5)
        else:
            r = requests.get(url, headers=headers , timeout=5 )
        with open(str(file), "wb") as code:
            code.write(r.content)
with open("downimgurl.txt" ,"r",encoding="utf-8") as f:
    y=f.read()
import time
e=y.split("\n")
x=True
while 1:
    e = y.split("\n")
    u=""
    try:
        print(len(e))
        for index,i in enumerate(e):
            print(index,i)
            u=i
            downloadfile(i)
        break
    except Exception as e:
        if x==True:
            x=False
        else:
            x=True
        print(e)
        print("err :",u)
        time.sleep(2)
        downloadfile(i)
        time.sleep(2)
        pass

