__author__ = 'yo'

class shop():
    def __init__(self):
        self.ping,self.gai,self.jiu=0,0,0
    def buyshui(self,p):
        self.ping,self.gai,self.jiu=p,p,p
        print("水{},空瓶{},盖子{}".format(self.jiu,self.ping,self.gai))
    @property
    def h_gai(self):
        t_jiu=int(self.gai/3)
        self.jiu=t_jiu+ self.jiu #一共多少瓶酒
        self.gai=t_jiu+self.gai%3#剩下的盖子
        self.ping=self.ping+t_jiu
        print("换盖后:水{},空瓶{},盖子{}".format(self.jiu,self.ping,self.gai))
    @property
    def h_ping(self):
        t_jiu=int(self.ping/2)
        self.jiu=t_jiu+ self.jiu
        self.ping=t_jiu+self.ping%2
        self.gai=self.gai+t_jiu
        print("换瓶后:水{},空瓶{},盖子{}".format(self.jiu,self.ping,self.gai))
d=shop()
d.buyshui(int(10))
while 1:
    if d.ping>1:d.h_ping
    if d.gai>2:d.h_gai
    if d.ping<2 and d.gai<3:break

#
# k=瓶+盖子+水
# k=kp+gz+s
# k=2kp
# k=3gz
# kp=gz+s
# 2gz=kp+s
# 2gz=gz+s+s
# gz=2s
# kp=(kp+s)/2+s
# 2kp=kp+3s
# kp=3s
# k=((kp+s)/2+s)2
# k=6s
#
# 已知条件
# kp=3s  空瓶 =3水
# gz=2s  盖子=2水
# k=6s
#
# 结果 应该是 水53,空瓶1,盖子2
# 水53 3s 4s
# 折算 53s+3s+4s
# k=6s
#
# k*10=6s*10
#
# 剩余   借      现  进  凑数还    账  折算成喝掉的
#
# 1 2     1     2 3  +2   -1       1   2s
# 1 1     1     2 2  +1   -1       0   1s
# 0 2     1     1 3  +1   -1       0   1s
# 1 0     1     2 1  +1   -1       0   1s
# 0 1     1     1 2  +0   -0      -1   1s
# 1 2     1     2 3  +2   -2       0   2s
#
#
#
# 53k=53kp+53gz+53s +kp+2gz
# 53k=54kp+55gz+53s
#
# 53k=53s+52p+51gz




