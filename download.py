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
        print(url)

        # time.sleep(0.5)

        if x==True:
            x=False
        else:
            x=True

        if x:
            url=url.replace("www","static")
            r = requests.get(url, headers=headers, timeout=5)
        else:
            r = requests.get(url, headers=headers , timeout=5 )
        if r and len(str(r))>1000:
            with open(str(file), "wb") as code:
                code.write(r.content)
from multiprocessing.dummy import Pool as ThreadPool
with open("downimgurl.txt" ,"r",encoding="utf-8") as f:
    y=f.read()
import time
e=y.split("\n")
x=True
err=0

with open("oo.txt","a",encoding="utf-8") as b:
    for i in e:
        k=check_path(i)
        if k:
            b.write("{}\n".format(k))


def a():
# while 1:
    for i in range(3):

        e = y.split("\n")
        u = ""
        # for index,i in enumerate(e):
        try:
            # time.sleep(10)
            # print(index,i)
            # u=i
            # downloadfile(i)
            pool = ThreadPool(8)  # Sets the pool size to 4
            # print(i)
            results = pool.map(downloadfile, e)
            pool.close()
            pool.join()
            err=0
    # break
        except Exception as ei:
            # err=err+1
            # if x==True:
            #     x=False
            # else:
            #     x=True
            print(ei)
            print("err :",u)
            # time.sleep(err*4)
            # if err>10:
            #     time.sleep(360)

            pass
        time.sleep(10)
# def ()
#             t = threading.Thread(target=check_ip, args=(new_ip, dst_port) )
#             t.start()
#             # 把新建的线程放到线程池
#             all_threads.append(t)
#     # 循环阻塞主线程，等待每一字子线程执行完，程序再退出
#     for t in all_threads:
#         t.join()

# pool = ThreadPool(8) # Sets the pool size to 4
# results = pool.map(downImg,data);
# pool.close();
# pool.join();
