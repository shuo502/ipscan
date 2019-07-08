import socket
import threading
import requests
import re

# 创建接收路由列表
routers = []
r2=[]

# 创建互斥锁
lock = threading.Lock()

# 设置需要扫描的端口号列表
port_list = ['80','8080','21','22','23','3389','3306','27017','1433','1521','5001','5000','9000']


# 定义查询路由函数
def search_routers(a):
    # 获取本地ip地址列表
    local_ips = socket.gethostbyname_ex(socket.gethostname())[2]
    # print(local_ips)
    # 存放线程列表池
    all_threads = []
    # 循环本地网卡IP列表
    for ip in local_ips:
        ip='107.172.99.187'
        ip='172.246.62.66'
        # array[2]=str(97)
        # for i in range( 128,255):
        for i in range(185, 189):
            # 把网卡IP"."进行分割,生成每一个可用地址的列表
            # if int(array[2])<105:
            #     array[2]=str(int(array[2])+1)
            # 获取分割后的第四位数字，生成该网段所有可用IP地址
            array = ip.split('.')

            array[3] = str(i)
            # 把分割后的每一可用地址列表，用"."连接起来，生成新的ip
            new_ip = '.'.join(array)
            # print(new_ip)
            # 遍历需要扫描的端口号列表
            for port in port_list:
                dst_port = int(port)
                # 循环创建线程去链接该地址
                t = threading.Thread(target=check_ip, args=(new_ip, dst_port,a) )
                t.start()
                # 把新建的线程放到线程池
                all_threads.append(t)
    # 循环阻塞主线程，等待每一字子线程执行完，程序再退出
    for t in all_threads:
        t.join()


def r_check_ip(ip_portlist):
    all_threads=[]
    for ip_port in ip_portlist:
        # 循环创建线程去链接该地址
        t = threading.Thread(target=check_ip, args=(ip_port[0],443) )
        t.start()
        # 把新建的线程放到线程池
        all_threads.append(t)
    # 循环阻塞主线程，等待每一字子线程执行完，程序再退出

    for t in all_threads:
        t.join()


# 创建访问IP列表方法
def check_ip(new_ip, port,a):
    # 创建TCP套接字，链接新的ip列表
    scan_link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置链接超时时间
    scan_link.settimeout(5)
    # 链接地址(通过指定我们 构造的主机地址，和扫描指定端口)
    result = scan_link.connect_ex((new_ip, port))
    #
    scan_link.close()
    # print(result)
    # 判断链接结果
    if result == 0:
        # 加锁
        lock.acquire()
        # get(new_ip)
        if a:a.write("{}:{}\n".format(new_ip,port))

        print(new_ip, '\t\t端口号%s开放' % port)
        # print(new_ip)
        routers.append((new_ip, port))
        # 释放锁
        lock.release()
    # print(routers)

print("正在扫描..., 请稍等...")
def get(host):
    url='http://{}'.format(host)
    try:
        s=requests.get(url, timeout=2)
        print(s.content)
    except Exception  as e:
        s_r=e.args[0]
        if 'hostname' in str(s_r):
            try:
                b=s_r.rfind("doesn't match")
                r=re.compile(r'\'(.*?)\'')
                print("{}:{}:  {}".format(host,r.findall(s_r[b:])),s_r )
            except:
                print(s_r)
    # if s.status_code == 0:
    #     # 加锁
    #     lock.acquire()
    #     # get(new_ip)
    #     # print(new_ip, '\t\t端口号%s开放' % port)
    #     # print(new_ip)
    #     # routers.append((new_ip, port))
    #     # 释放锁
    #     lock.release()
# def get_ip(ip_portlist):
#     all_threads=[]
#     for ip_port in ip_portlist:
#         # 循环创建线程去链接该地址
#         t = threading.Thread(target=get, args=(ip_port[0]) )
#         t.start()
        # 把新建的线程放到线程池
    #     all_threads.append(t)
    # # 循环阻塞主线程，等待每一字子线程执行完，程序再退出
    #
    # for t in all_threads:
    #     t.join()
# 启动程序入口
if __name__ == '__main__':
    # 启动扫描程序
    # port_list=[80]

    # with open("ip.txt",'a',encoding='utf-8') as a:
    #     search_routers(a)
    a=None
    search_routers(a)
    # print(routers)
    # r_check_ip(routers)
    # print(routers)
    import time
    # x=[('107.172.102.9', 80), ('107.172.102.4', 80), ('107.172.102.3', 80), ('107.172.102.7', 80), ('107.172.102.19', 80), ('107.172.102.11', 80), ('107.172.102.13', 80), ('107.172.102.20', 80), ('107.172.102.22', 80), ('107.172.102.17', 80), ('107.172.102.12', 80), ('107.172.102.26', 80), ('107.172.102.58', 80), ('107.172.102.61', 80), ('107.172.102.54', 80), ('107.172.102.39', 80), ('107.172.102.36', 80), ('107.172.102.47', 80), ('107.172.102.156', 80), ('107.172.102.133', 80), ('107.172.102.141', 80), ('107.172.102.160', 80), ('107.172.102.159', 80), ('107.172.102.143', 80), ('107.172.102.149', 80), ('107.172.102.154', 80), ('107.172.102.167', 80), ('107.172.102.153', 80), ('107.172.102.190', 80), ('107.172.102.182', 80), ('107.172.102.144', 80), ('107.172.102.170', 80), ('107.172.102.163', 80), ('107.172.102.173', 80), ('107.172.102.199', 80), ('107.172.102.204', 80), ('107.172.102.218', 80), ('107.172.102.217', 80), ('107.172.102.213', 80), ('107.172.102.227', 80), ('107.172.102.241', 80), ('107.172.102.238', 80), ('107.172.102.242', 80), ('107.172.102.211', 80), ('107.172.102.245', 80), ('107.172.102.239', 80), ('107.172.102.246', 80), ('107.172.102.250', 80)]
    # for i in x:
    #     u=i[0]
    #     get(u)
    # 98255 99128
    # 100128