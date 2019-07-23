# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 16:51
# @Author  : Yo
# @Email   : shuo502@163.com
# @File    : createcode128png.py
# @Software: PyCharm
# @models: ..
# @function: ...
# @Git: https://gitee.com/m7n9/PyCharm.git
# @Edit: yo


import code128

with open("code.txt",'r',encoding='utf-8') as f:
    y=f.read()

for i in y.split("\n"):
    print(i)
    if len(i):
        file="./code/{}.png".format(i)
        code128.image(str(i)).save(file)  # with PIL present