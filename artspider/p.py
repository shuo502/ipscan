__author__ = 'yo'

import base64 as b64
import base64
def rb_pic_to_base64_pic():
    with open("1.png",'rb') as f:
        base64_data = base64.b64encode(f.read())
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
