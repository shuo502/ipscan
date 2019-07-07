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
        "http2": 82,
        "http3": 88,
        "http4": 8000,
        "http5": 8080,
        "http6": 8888,
        "http7": 888,
        "http8": 9000,
        "http9": 5000,
        "http10": 1080,
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
    port = {'mongodb': 27017,
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
        "ftp": 21,
        "ssh": 22,
        "telnet": 23,
    }
    return port


def p_app():
    # qq 金万维
    port = {
        "qq": 4000,
        "jww": 5366,
        "ntp": 123,
        "dns": 53,

    }
    return port


# 定义查询路由函数
def search_routers(port_list,ip="107.172.99.187",t_s=1,t_e=254):
    all_threads = []
    for i in range(t_s,t_e+1):
        array = ip.split('.')
        array[3] = str(i)
        new_ip = '.'.join(array)
        if int(t_e)==1:
            new_ip=ip
        for port in port_list:
            dst_port = int(port_list[port])
            # 循环创建线程去链接该地址

            t = threading.Thread(target=check_ip, args=(new_ip, dst_port) )
            t.start()
            # 把新建的线程放到线程池
            all_threads.append(t)

    # 循环阻塞主线程，等待每一字子线程执行完，程序再退出
    for t in all_threads:
        t.join()


# 创建访问IP列表方法
def check_ip1(new_ip, port):
    sem.acquire()#上锁

    # 创建TCP套接字，链接新的ip列表
    scan_link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置链接超时时间
    scan_link.settimeout(8)
    # 链接地址(通过指定我们 构造的主机地址，和扫描指定端口)
    result = scan_link.connect_ex((new_ip, port))
    #
    scan_link.close()
    # print(result)
    # 判断链接结果
    if result == 0:
        # 加锁

        # get(new_ip)
        # if a:a.write("{}:{}\n".format(new_ip,port))

        # print(new_ip, '\t\t端口号%s开放' % port)
        # print(new_ip)
        routers.append((new_ip, port))
        if new_ip in scan_dict:
            scan_dict[new_ip].append(port)
        else:
            scan_dict[new_ip]=[]
            scan_dict[new_ip].append(port)
        print( new_ip,scan_dict[new_ip] )
        # 释放锁
        lock.release()

    # print(routers)

import time
def check_ip(new_ip, port):
    sem.acquire()#上锁
    time.sleep(5)
    scan_link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_link.settimeout(8)
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
    sem=threading.Semaphore(100)
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
    ips='172.247.198.153'
    search_routers(port_list=port_list,ip=ips)
    for i in scan_dict:
        y=sorted(scan_dict[i])
        print(i,y)

    # 设置需要扫描的端口号列表
    # port_list = ['80','8080','21','22','23','3389','3306','27017','1433','1521','5001','5000','9000']



