# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 18:36
# @Author  : Yo
# @Email   : shuo502@163.com
# @File    : seleniumdemo.py
# @Software: PyCharm
# @models: ..
# @function: ...
# @Git: https://gitee.com/m7n9/PyCharm.git
# @Edit: yo


from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
path = "/chromedriver"
driver = webdriver.Chrome(path)
driver=driver.ChromeOptions()
driver.add_argument('--headless')
driver.add_argument('--no-sandbox')
driver.add_argument('--disable-gpu')
driver.add_argument('--disable-dev-shm-usage')

driver.get("http://t.tjdcd.com")
print(driver.page_source)
driver.quit()
display.stop()
