__author__ = 'yo'
#coding=utf-8
import threading

class scanner(threading.Thread):
    tlist=[] #用来存储队列的线程
    maxthreads=5 # int(sys.argv[2])最大的并发数量，此处我设置为100，测试下系统最大支持1000多个
    evnt=threading.Event()#用事件来让超过最大线程设置的并发程序等待
    lck=threading.Lock() #线程锁
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            pass
        except Exception as e:
            print (e.message)
        #以下用来将完成的线程移除线程队列
        scanner.lck.acquire()
        scanner.tlist.remove(self)
        #如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(scanner.tlist)==scanner.maxthreads-1:
            scanner.evnt.set()
            scanner.evnt.clear()
        scanner.lck.release()

    def newthread(counter):
        scanner.lck.acquire()#上锁
        sc=scanner()
        # sc.Thread( )
        scanner.tlist.append(sc)
        scanner.lck.release()#解锁

        sc.start()
    #将新线程方法定义为静态变量，供调用
    newthread=staticmethod(newthread)

def runscan():
    for i in range(1,1000):
        scanner.lck.acquire()
        #如果目前线程队列超过了设定的上线则等待。
        if len(scanner.tlist)>=scanner.maxthreads:
            print("222222222222222222")
            scanner.lck.release()
            scanner.evnt.wait()#scanner.evnt.set()遇到set事件则等待结束
        else:
            scanner.lck.release()
            global x
            x=x+1
            scanner.newthread(proxy(x))
    for t in scanner.tlist:
        t.join()#join的操作使得后面的程序等待线程的执行完成才继续
import requests
def proxy(counter):
    requests.head("http://192.168.0.1")
    print(counter)
    time.sleep(3)
    print(counter)
if __name__=="__main__":
    import time
    x=0
    runscan()