__author__ = 'yo'
import threading
import time
sem=threading.Semaphore(4)
def search_routers(port_list,ip="107.172.99.187",t_s=1,t_e=254):
    all_threads = []

    for i in range(t_s,t_e+1):
        array = ip.split('.')
        array[3] = str(i)
        new_ip = '.'.join(array)
        if int(t_e)==1:
            new_ip=ip
        # with   sem:
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
import datetime
def check_ip(i,j):
    sem.acquire()#上锁
    print(datetime.datetime.now())
    time.sleep(2)
    print("--")
    print("check_ip{} {}".format(i,j))
    print("1--")
    sem.release()#解锁


port_list= {
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
search_routers(port_list=port_list,t_e=254)
# sem=threading.Semaphore(4)  #限制线程的最大数量为4个
#
# def gothread():
#     with  sem:  #锁定线程的最大数量
#         for i in range(8):
#             print(threading.current_thread().name,i)
#             time.sleep(1)
#
# for i in range(5):
#     threading.Thread(target=gothread).start()
