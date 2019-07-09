__author__ = 'yo'
import requests
import re
arturl={}
pageurl={}
url="https://whois.ipip.net/AS36352"
# r=requests.get(url)
# t=r.content.decode()
# print(t)
import base64 as b64
import base64
def rb_pic_to_base64_pic():
    base64_data = base64.b64encode()
    s = base64_data.decode()
    print('data:image/jpeg;base64,%s'%s)


def base64_pic_to_localpic():
    sss ="""/9j/4AAQSkZJRgABAQEASABIAAg8MEBcUGBgXFBYWGh0lHxobIxwWshDahuOQq6EH//Z"""
    print(len(sss))
    imagedata = base64.b64decode(sss)
    print(imagedata)
    file = open('1.jpg',"wb")
    file.write(imagedata)
    file.close()

x=21
j=1
for i in range(24-x):
    j=j*2
    t=j-1

print(t)
e=0
for i in range(t+1):
   e=e+256
print(e-1-t)