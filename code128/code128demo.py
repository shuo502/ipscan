# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 16:46
# @Author  : Yo
# @Email   : shuo502@163.com
# @File    : code128demo.py
# @Software: PyCharm
# @models: ..
# @function: ...
# @Git: https://gitee.com/m7n9/PyCharm.git
# @Edit: yo


import code128

code128.image("CUKe3DGg").save("Hello World.png")  # with PIL present
#
with open("Hello World.svg", "w") as f:
        f.write(code128.svg("Hello World"))