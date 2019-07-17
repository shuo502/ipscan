# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 15:59
# @Author  : Yo
# @Email   : shuo502@163.com
# @File    : suan.py
# @Software: PyCharm
# @models: ..
# @function: ...
# @Git: https://gitee.com/m7n9/PyCharm.git
# @Edit: yo


class daili():
    def __init__(self):
        self.name = ""
        self.qian = 0
        self.huokuan = 0
        self.dengji = 99
        self.zk = 10
        self.updl = ""
        self.downdl = []
        self.downdl_huokuan = 0  # 总计下级代理结余货款 发展的下线手上的货款
        self.downdl_dslirun = 0#待收利润
        self.downdl_huikuan=0 # 总计下级代理销售
        self.downdl_yslirun = 0#已收利润
        self.downdl_txlirun = 0#提现利润
    @property
    def dengji_baozhengjin(self):
        if 600000 <= self.qian:
            self.dengji = 0
            self.zk = 2.5
        if 90000 <= self.qian < 600000:
            self.dengji = 1
            self.zk = 3.5
        if 30000 <= self.qian < 90000:
            self.dengji = 2
            self.zk = 5
        if 10000 <= self.qian < 30000:
            self.dengji = 3
            self.zk = 7

    def test_dengjibaozhengjin(self,qian):
        if 600000 <= qian:
            dengji = 0
            zk = 2.5
        if 90000 <= qian < 600000:
            dengji = 1
            zk = 3.5
        if 30000 <= qian < 90000:
            dengji = 2
            zk = 5
        if 10000 <= qian < 30000:
            dengji = 3
            zk = 7
        return [dengji,zk]

    def set_updl(self, name):
        print("原来上级代理:{}，现在上级代理:{}".format(self.updl, name))
        self.updl = name
    @property
    def has_updl(self):
        if len(self.updl):
            return True
        else:
            return False
    @property
    def has_downdl(self):
        if len(self.downdl):
            return True
        else:
            return False

    def buy(self, pp):
        print("购买支出{}".format(pp))
        "如果有上级代理通知上级代理记录销售扣减折算利润"
        self.huokuan = self.huokuan - pp

    def jiaoqian(self, qian, name=""):
        if len(name) > 0:
            self.name = name
        self.qian = qian + self.qian
        self.dengji_baozhengjin
        huokuan = float('%.2f' % (float(qian / self.zk * 10)))

        self.huokuan = self.huokuan + huokuan

        print("{}这次交钱{},总共交钱{},折算成货款{}".format(name, qian, self.qian, self.huokuan))

    def fx_daili(self, dailiqian, name):
        # 发展了下线，通知上线增加待收利润，增加下线代理商货款
        #按我的折扣去上线购买一批货，代理按照代理去找上级购买一批货。

        self.downdl.append(name)
        fxdailijbie_zk=self.test_dengjibaozhengjin(dailiqian)[1]
        print("增加代理：{}代理折扣{}，代理交钱,{}".format(name, fxdailijbie_zk, dailiqian))
        zjnh =float('%.2f' % float(dailiqian / self.zk * 10))# dailiqian / (fxdailijbie_zk - self.zk) * 10
        dlnh =float('%.2f' % float( dailiqian / fxdailijbie_zk * 10))
        daililirun=float('%.2f' % float(zjnh-dlnh))/10*self.zk
        self.downdl_huokuan = float('%.2f' % float(self.downdl_huokuan + dlnh))
        self.downdl_dslirun=daililirun+self.downdl_dslirun #发展代理可能带来的利润
        # self.huokuan = float('%.2f' % float(self.huokuan + daililirun))

        print("自己{}拿货款{}分给下级代理货款{}自己增加代理盈余货款{},自己总货款{}".format(self.zk,zjnh,dlnh,daililirun, self.huokuan))
        print("代理全部销售完自己可获{}下级代理可获得利润{}".format(daililirun*self.zk/10,dlnh*(1-fxdailijbie_zk/10)))
        pass

    def xia_tui_daili(self,xiadailihuokuan,xiadailizhekou,dlhk=0,ys=0,yt=0,dslr=0):
        #下线退了 扣除 上线 待收利润 扣除下线代理商货款
        #退的代理按他的折扣找我退款，然后 我按我的折扣去找上线退款。

        # 货款 已收，已提 代收利润
        "是否有上级，上级折扣。换算上级盈利货款  扣除货款，扣除待回收利润"
        print("下级退代理前 我的包含代理利润的货款{}我的代理待收利润{}我所有下级代理的货款{}".format(self.huokuan,self.downdl_dslirun,self.downdl_huokuan))
        print("下级退代理 货款{} 折扣 {}下级发展的代理利润货款{}".format(xiadailihuokuan,xiadailizhekou,dslr))

        # 应该退
        #待收 已收，已提
        tui_xiadailiqian=float('%.2f' %float(xiadailihuokuan*xiadailizhekou/10))
        tui=tui_xiadailiqian+ys-yt
        self.downdl_dslirun=self.downdl_dslirun+dslr
        print("存在的利润款{}".format(((tui_xiadailiqian / self.zk * 10)-(tui_xiadailiqian / xiadailizhekou * 10))/10*self.zk))

        selflr=tui_xiadailiqian  - tui_xiadailiqian / xiadailizhekou  * self.zk

        if self.has_updl:
            pass
        self.downdl_dslirun=float('%.2f' %float(self.downdl_dslirun-(((tui_xiadailiqian / self.zk * 10)-(tui_xiadailiqian / xiadailizhekou * 10))/10*self.zk)))
        self.downdl_huokuan = self.downdl_huokuan -xiadailihuokuan  # 总计下级代理结余货款 发展的下线手上的货款

        self.downdl_huikuan=float('%.2f' %float(self.downdl_huikuan)) # 总计下级代理销售


        print("下级退代理费用{}".format(tui_xiadailiqian))
        print("下级退代理后 我的货款包含所有代理利润的货款{}我的代理待收利润{}我所有下级代理的货款{}".format(self.huokuan,self.downdl_dslirun,self.downdl_huikuan))
        # 下级的货款 折算
        # "下级代理是否还有下级。扣除下级的下级代理利润货款(利润折现货款)"
        pass


    def self_tui_daili(self):
        if self.has_updl:
            #通知上级增加待收利润，通知上级增加 下级代理货款金额，通知上级减少 代理货款。
            "通知上级代理扣除折算货款利润"
        if self.has_downdl:
            # 通知下级更换上级代理。
            "下级总货款+"
            "扣除下级加盟未消费利润"
        pass

    def self_sell(self):
        # 通知上级我卖多少钱，我的级别。
        if self.has_updl:

            pass
        pass

    def down_daili_sell(self,pp,zk):

        self.downdl_huokuan = self.downdl_huokuan-pp  # 总计下级代理结余货款 发展的下线手上的货款
        lr=pp - pp / zk * self.zk

        print("下级销售本级获得利润:{}".format(lr))
        self.downdl_dslirun = self.downdl_dslirun-lr#待收利润
        self.downdl_huikuan=self.downdl_huikuan+pp # 总计下级代理销售
        self.downdl_yslirun = self.downdl_yslirun+lr#已收利润

        # self.downdl_huokuan = self.downdl_huokuan-pp # 总计下级代理结余货款
        # self.downdl_dslirun = self.downdl_kslirun
        # self.downdl_yslirun = self.downdl_kslirun
        # self.downdl_txlirun = self.downdl_kslirun
        # self.downdl_huikuan = self.downdl_huikuan+pp  # 总计下级代理销售

    def look_self(self):
        a="名字：{}充值：{}货款：{}等级：{}折扣：{}上级：{}下级：{}下级总货款：{}待收利润：{}总计销售：{}已收利润：{}已提利润：{}".format(self.name ,self.qian , self.huokuan,self.dengji , self.zk ,self.updl ,self.downdl,self.downdl_huokuan ,  self.downdl_dslirun, self.downdl_huikuan ,self.downdl_yslirun , self.downdl_txlirun)
        print(a)
    @property
    def look_lirun(self):
        lr = float('%.2f' % float(((self.qian / a.zk) * 10 - (self.huokuan-self.downdl_huokuan)) * (1 - a.zk / 10)))
        print("已提直接销售利润{}".format(lr))
        return lr

    @property
    def look_dengji(self):
        print("代理等级{}".format(self.dengji))
        return self.dengji

    @property
    def look_zk(self):
        print("实行折扣{}".format(self.zk))
        return self.zk

    @property
    def look_huokuan(self):
        print("可用货款{}".format(self.huokuan))
        return self.huokuan


class chanp():
    cp1 = 1000
    cp2 = 2000


a = daili()
a.jiaoqian(90000)
a.look_dengji
a.look_zk
a.look_huokuan

a.buy(chanp.cp1)
a.look_huokuan

a.look_lirun

a.fx_daili( 10000, "小王")

a.look_self()
a.down_daili_sell(chanp.cp1,7)
a.xia_tui_daili(14285.71,7,0)

a.look_self()

