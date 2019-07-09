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
d.buyshui(int(5))
while 1:
    if d.ping>1:d.h_ping
    if d.gai>2:d.h_gai
    if d.ping<2 and d.gai<3:break

