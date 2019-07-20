__author__ = 'yo'
import string
import random

KEY_LEN = 5
KEY_ALL = 150


def base_str():
    print(string.ascii_letters + string.digits)
    return (string.ascii_letters + string.digits)


def key_gen():
    keylist = [random.choice(base_str()) for i in range(KEY_LEN)]
    print(keylist)
    return ("".join(keylist))


def key_num(num, result=None):
    if result is None:
        result = []
    for i in range(num):
        result.append(key_gen())
    return result


def print_key(num):
    r=[]
    for i in key_num(num):
        print(i)
        r.append(i)
    return r


if __name__ == "__main__":
    # e=print_key(KEY_ALL)
    s=str(string.ascii_letters + string.digits)
    print(len(s))
    # o=[]
    # for j in e:
    #     if j not in o:
    #         o.append("CUK"+j)
    # print(o)
    # print(len(o))
    # with open("ckey.txt", "a",encoding="utf-8") as f:
    #
    #     for i in o:
    #         f.write(i+"\n")