__author__ = 'yo'
import requests
# url='https://107.172.103.51'
# url='https://107.172.99.144'
# url='https://107.172.103.206'
import re
def get(host):
    url='https://{}'.format(host)
    try:
        s=requests.head(url)
        print(s.content)
    except Exception  as e:
        if "SSLCertVerificationError" in str(e):
            e=str(e.args[0])
            print(e)
            b=e.rfind("match either of")
            if b:
                r=re.compile(r'\'(.*?)\'')
                arr_x=r.findall(e[b:])
                if arr_x:
                    arr_x.append(host)
                    print(arr_x)
        else:
             pass
all='''107.172.99.132
107.172.99.144
107.172.99.153
107.172.99.154
107.172.99.190
107.172.99.155
107.172.99.189'''
list=all.split("\n")
# print(list)
# for i in list:
#     print(get(i))
# HTTPSConnectionPool(host='107.172.103.206', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1051)')))
get('107.172.99.144')
x="""HTTPSConnectionPool(host='107.172.99.144', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError("hostname '107.172.99.144' doesn't match either of 'countrymoments.net', 'www.countrymoments.net'")))
"""




