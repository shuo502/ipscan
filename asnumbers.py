__author__ = 'yo'
import requests
import os
import re
url="https://www.iana.org/assignments/as-numbers/as-numbers.txt"
r=requests.get(url).content.decode()
with open("AS.txt","a",encoding="utf-8") as f:
    f.write(r)
