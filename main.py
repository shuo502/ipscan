__author__ = 'yo'

import socket
import threading
import requests
import re

# 创建接收路由列表
routers = []
r2=[]

# 创建互斥锁


def p_webopen():
    port = {
        "http0": 80,
        "http1": 81,
        # "http2": 82,
        "http3": 88,
        "http4": 8000,
        "http5": 8080,
        "http6": 8888,
        "http7": 888,
        # "http8": 9000,
        # "http9": 5000,
        # "http10": 1080,
    }
    pass
    return port


def p_sslwebopen():
    port = {
        "ssl": 443
    }
    pass
    return port


def p_dbopen():
    port = {
        'mongodb': 27017,
            'oracle': 1521,
            'mongodb2': 2888,
            'mysql': 3306,
            "mssql": 1433

            }
    pass
    return port


def p_manage():
    # ftp ssh  telnet
    port = {
        # "ftp": 21,
        "ssh": 22,
        # "telnet": 23,
    }
    return port


def p_app():
    # qq 金万维
    port = {
        # "qq": 4000,
        # "jww": 5366,
        # "ntp": 123,
        # "dns": 53,

    }
    return port


# 定义查询路由函数
def search_routers(port_list,ip="107.172.99.187",t_s=1,t_e=254):
    all_threads = []
    for port in port_list:
        for i in range(t_s, t_e + 1):
            array = ip.split('.')
            array[3] = str(i)
            new_ip = '.'.join(array)
            if int(t_e) == 1:
                new_ip = ip
            dst_port = int(port_list[port])
            t = threading.Thread(target=check_ip, args=(new_ip, dst_port) )
            t.start()
            all_threads.append(t)

    # 循环阻塞主线程，等待每一字子线程执行完，程序再退出
    for t in all_threads:
        t.join()


import time
def check_ip(new_ip, port):
    sem.acquire()#上锁
    time.sleep(5)
    scan_link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_link.settimeout(4)
    result = scan_link.connect_ex((new_ip, port))
    scan_link.close()
    if result == 0:
        routers.append((new_ip, port))
        if new_ip in scan_dict:
            scan_dict[new_ip].append(port)
        else:
            scan_dict[new_ip]=[]
            scan_dict[new_ip].append(port)
        print( "{}:{}".format(new_ip,scan_dict[new_ip] ))
    sem.release()#解锁

if __name__ == "__main__":
    lock = threading.Lock()
    sem=threading.Semaphore(3)
    scan_dict={}
    port_list = {}
    p=p_app()
    port_list = dict(port_list, **p)
    p=p_dbopen()
    port_list = dict(port_list, **p)
    p=p_manage()
    port_list = dict(port_list, **p)
    p=p_sslwebopen()
    port_list = dict(port_list, **p)
    p=p_webopen()
    port_list = dict(port_list, **p)
    ips='172.246.62.161'
    search_routers(port_list=port_list,ip=ips,t_s=158,t_e=170)
    with open("ip.txt", "a", encoding="utf-8") as ipfile:
        for i in scan_dict:
            y=sorted(scan_dict[i])
            e="{}:{}\n".format(i,y)
            print(e)
            ipfile.write(e)
    # for i
    # 设置需要扫描的端口号列表
    # port_list = ['80','8080','21','22','23','3389','3306','27017','1433','1521','5001','5000','9000']



