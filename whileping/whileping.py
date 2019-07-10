#conding=UTF-8
import os
import subprocess
import datetime
#

def ping():
    global wan_net, route_net, lan_net,savefile
    lost_status=0
    j=0
    proc = subprocess.Popen(wan_net, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    open(savefile, "a", encoding="utf-8").write("\nSTART:{}\n\n启动时会丢失2个包\n".format(str(datetime.datetime.now())[:19]))
    print("程序已经启动\n外网:{}\n路由:{}\n内网:{}\n检测日志文件:{}".format( wan_net, route_net, lan_net,savefile))
    for line in iter(proc.stdout.readline, 'b'):
        secret = line.decode('gbk', errors="ignore")
        # print(secret)
        if len(secret)==0:
            break
        if "ms" in  secret:
            lost_status = 0
        else:
            t=str(datetime.datetime.now())[:19]
            lan_net,route_net="内网正常","路由正常"
            b = os.popen(route_net)
            if "ms" in str(b.readlines()):
                pass
            else:
                route_net="路由断开"
                a = os.popen(lan_net)
                if "ms" in str(a.readlines()):
                    pass
                else:
                    lan_net="内网断开"
            if lost_status==0:
                j=j+1
            lost_status=lost_status+1
            w_net="外网断开  第{}次丢包连续丢包第{}包 \n".format(j,lost_status)
            ret="{} - {} - {} - {}".format(t,lan_net ,route_net ,w_net)
            with open(savefile,"a",encoding="utf-8") as f:
                f.write(ret)
    proc.stdout.close()


wan_net='ping t.tjdcd.com -w 400 -t '
route_net="ping 10.0.0.1 -n 2 -w 5"
lan_net="ping 172.16.0.1 -n 2 -w 5"
savefile="log.txt"
ping()
# b = os.popen(route_net)
# print(str(b.readlines()))