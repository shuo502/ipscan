# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 17:07
# @Author  : Yo
# @Email   : shuo502@163.com
# @File    : pyqrccodedemo.py
# @Software: PyCharm
# @models: ..
# @function: ...
# @Git: https://gitee.com/m7n9/PyCharm.git
# @Edit: yo


import pyqrcode
# import pypng #不安装不能保存png
url = pyqrcode.create('http://uca.edu', error='L')#H Q M L 容错率
# url.svg('uca-url.svg', scale=8)
# url.eps('uca-url.eps', scale=2)
url.png('uca-url8.png', scale=8)#保存图片缩放
# url.png('uca-url7.png', scale=7)
# url.png('uca-url6.png', scale=6)
# url.png('uca-url5.png', scale=5)
# url.png('uca-url4.png', scale=4)
# url.png('uca-url3.png', scale=3)
# url.png('uca-url2.png', scale=2)
# print(url.terminal(quiet_zone=1))
#
# big_code = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
# big_code.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
# big_code.show()