__author__ = 'yo'
import requests
url="http://site.ip138.com/107.172.102.20"
url="https://dns.aizhan.com/139.199.104.203/"
url="https://tools.ipip.net/ipdomain.php"
# r=requests.get(url)
r=requests.post(url,data={'ip':'139.199.104.20'})
sr=r.content.decode(r.encoding)
print(sr)
print(r.cookies)
r=requests.post(url,data={'ip':'107.172.102.246'},cookies=r.cookies)
print(sr)
# print(sr[sr.find("result result"):sr.rfind("result result1")])
# print(sr[sr.find("<tbody>"):sr.rfind("</tbody>")])