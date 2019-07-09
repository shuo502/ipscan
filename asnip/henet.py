__author__ = 'yo'
#!/usr/bin/python
# coding=UTF-8
# Code by Anle

import os
import sys
import urllib
# import urllib2
import socket
from Lib import struct
import requests
from pyquery import PyQuery


def _usage():
    print ('Usage:\r\n BGP.py [Host]|IP-IP|Host.txt <-dns>\r\n')

def QueryRequest(szKeyword,iType=0):
    reCount = 0
    QueryUrl = 'http://bgp.he.net/search?search%5Bsearch%5D=' + urllib.quote(szKeyword) + '&commit=Search'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537'}
    while reCount < 3:
        try:
            # req = urllib2.Request(QueryUrl,headers=headers)
            # Resp = urllib2.urlopen(req)
            Resp=requests.get(QueryUrl,headers=headers)
            the_page = Resp.read()
            DOM = PyQuery(the_page)

            resList=[]

            if iType == 1:
                dns = DOM('#dns')("a")
                if dns:
                    for i in range(len(dns)):
                        resList.append(dns.eq(i).text())
                if len(resList) > 0:
                    print('[ %s : %d ]' % (szKeyword,len(resList)))
                    for i in range(len(resList)):
                        print(resList[i])
                return len(resList)

            trs1 = DOM('#search')("tbody")("tr")
            trs2 = DOM('#ipinfo')("tbody")("tr")

            if trs1:
                for i in range(len(trs1)):
                    p1 = trs1.eq(i)("td").children("a").text()
                    if p1=='' or p1.find('AS')>=0:
                        continue
                    p2 = trs1.eq(i)("td").next().text()
                    p3 = trs1.eq(i)("td").next().children("div").children("img").attr("title")
                    resList.append('{0:22}{1}\t{2}'.format(p1,p2,p3))
            elif trs2:
                for i in range(len(trs2)):
                    p1 = trs2.eq(i)("td").eq(1).text()
                    p2 = trs2.eq(i)("td").eq(2).text()
                    resList.append('{0:22}{1}'.format(p1,p2))
            else:
                resList = None
            if resList==None:
                print( '[-] %s - Not Result.' % szKeyword)
                return 0
            print( '\n[ %s : %d ]' % (szKeyword,len(resList)))
            for i in resList:
                print( i)
            return len(resList)
        except Exception as KeyboardInterrupt:
            print( '\n[!] User interrupt operation.\n')
            sys.exit(0)
        except:
            print( '[-] Connect to server failed.')
            reCount = reCount + 1
            print( ' Retrying %d\n' % reCount)

def _int2ip(num):
    strs = ''
    tt = [0,0,0,0]
    tt[0] = (num >> 24)
    tt[1] = ((num << 8) >> 24) % 256
    tt[2] = ((num << 16) >> 24) % 256
    tt[3] = ((num << 24) >> 24) % 256
    strs = '{0}.{1}.{2}.{3}'.format(tt[0],tt[1],tt[2],tt[3])
    return strs

def _ip2int(ip):
    num = 0
    ip = ip.split('.')
    num = int(ip[0]) * 256 ** 3 + int(ip[1]) * 256 ** 2 + int(ip[2]) * 256 + int(ip[3])
    return num

def BuildRange(strHost):
    dwStartIP = 0
    dwEndIP = 0
    print(strHost)
    if strHost.find('-')>0:
        ips = strHost.split('-')
        dwStartIP = _ip2int(ips[0])
        dwEndIP = _ip2int(ips[1])
    if strHost.find('/')>0:
        hosts = strHost.split('/')
        mask = int(hosts[1])
        dwStartIP = (_ip2int(hosts[0]) & (0xffffffff << (32-mask))) + 1
        dwEndIP = dwStartIP + (0xffffffff >> mask) - 2
    else:
        dwStartIP = dwEndIP = _ip2int(strHost)
    return [dwStartIP,dwEndIP]

def BuildHostRange(strHost):
    slash=[]
    startIpStr=""
    endIpStr=""
    ranges=0
    submask=0

    realStartIP=0
    realEndIP=0
    print(strHost)
    if strHost.find('-')>0:
        slash = strHost.split('-')
        startIpStr=slash[0]
        endIpStr=slash[1]
    else:
	    startIpStr=strHost
    try:
        startIpStr=socket.gethostbyname(startIpStr)
        if strHost.find('-')>0:
            realStartIP = socket.ntohl(struct.unpack('I',socket.inet_aton(startIpStr))[0])
            realEndIP = socket.ntohl(struct.unpack('I',socket.inet_aton(endIpStr))[0])
        else:
            realStartIP=realEndIP=socket.ntohl(struct.unpack('I',socket.inet_aton(startIpStr))[0])
    except:
        return [0,0]

    return [realStartIP,realEndIP]

def ParseResult(argKeyword,iType=0):
    info = []
    if os.path.exists(argKeyword):
        try:
            fs = open(argKeyword,'r')
            for line in fs:
                line = line.strip()
                QueryRequest(line,iType)
            fs.close()
        except:
            print ('Open file "%s" failed!' % argKeyword)
    elif argKeyword.find('-') > 0 or argKeyword.find('/') > 0:
        IpRange=BuildRange(argKeyword)
        for index in range(IpRange[0],IpRange[1]+1):
            curIP=_int2ip(index)
            QueryRequest(curIP,iType)
    else:
        QueryRequest(argKeyword,iType)

if __name__ == '__main__':
    # argLen = len(sys.argv)
    s=["","132.232.249.247"]
    argLen = len(s)

    if argLen < 2:
        _usage()
        sys.exit(0)
    # arg=sys.argv
    arg=s
    iType = 0
    if argLen >= 3:
        if arg[2]=='-dns':
            iType = 1
    ParseResult(arg[1],iType)
