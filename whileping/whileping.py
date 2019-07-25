#conding=UTF-8
import os
import subprocess
import datetime
#

def ping():
    global wan_net, route_net, lan_net,savefile
    try:
        lost_status=0
        j=0
        proc = subprocess.Popen(wan_net, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        open(savefile, "a", encoding="utf-8").write("\nSTART:{}\n\n启动时会丢失2个包\n".format(str(datetime.datetime.now())[:19]))
        print("网络状况监控程序已经启动,请勿关闭\n{}\n外网:{}\n路由:{}\n内网:{}\n检测日志保存文件:{}".format( str(datetime.datetime.now())[:19],wan_net, route_net, lan_net,savefile))
        for line in iter(proc.stdout.readline, 'b'):
            secret = line.decode('gbk', errors="ignore")
            # print(secret)
            if len(secret)==0:
                break
            if "ms" in  secret:
                lost_status = 0
            else:
                t=str(datetime.datetime.now())[:19]
                lan_net_p="内网正常"
                route_net_p="路由正常"
                b = os.popen(route_net)
                if "ms" in str(b.readlines()):
                    pass
                else:
                    route_net_p="路由断开"
                    a = os.popen(lan_net)
                    if "ms" in str(a.readlines()):
                        pass
                    else:
                        lan_net_p="内网断开"
                if lost_status==0:
                    j=j+1
                lost_status=lost_status+1
                w_net_p="外网断开  第{}次丢包连续丢包第{}包 \n".format(j,lost_status)
                ret="{} - {} - {} - {}".format(t,lan_net_p ,route_net_p ,w_net_p)
                with open(savefile,"a",encoding="utf-8") as f:
                    f.write(ret)
    except:
        ping()
    proc.stdout.close()


wan_net='ping baidu.com -w 400 -t '
route_net="ping 10.0.0.1 -n 1 -w 5"
lan_net="ping 172.16.0.1 -n 1 -w 5"
savefile="log.txt"

ping()

# b = os.popen(route_net)
# print(str(b.readlines()))
