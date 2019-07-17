import tkinter, win32api, win32con, pywintypes,datetime

def get_replicate_text(text):
    # i, space, str1, str2 = 0, 70, "", ""
    # while (i <= 5):
    #     str1 = str1 + text + " " * space
    #     i = i + 1
    # str2 = " " * space + str1 + "\n\n\n\n"
    # str1 = str1 + "\n\n\n\n"
    # str1 = (str1 + str2) * 5
	str1=text
	return str1


root = tkinter.Tk()
root.overrideredirect(True)
root.geometry("+1100+160") #设置窗口位置或大小
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")#白色背景透明
hWindow = pywintypes.HANDLE(int(root.frame(), 16))
exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
# E:/1.gif 156 0.02
# E:/2.gif 75 0.04
# E:/3.gif 60 0.03
# E:/4.gif 4 0.1
# E:/5.gif 136 0.02
# E:/6.gif 144 0.03
# E:/9.gif 36 0.05
framenum = 36 # gif 的帧数需要确定下来
giffile = 'E:/9.gif' #找一张白色背景的gif，设置白色为透明
frame_s=100
frames = [tkinter.PhotoImage(file=giffile,format = 'gif -index %s' % i) for i in range(framenum)]
x=1440
y=960

xj=True
yj=True
mx=0
my=0
mt=0
xt=0
yt=0

import random
import cmath
def random_m():
	global mx,my,juli,mt,tx,ty
	tx=x
	ty=y
	mx=random.randint(1,1440)
	my=random.randint(1,960)
	juli=int(cmath.sqrt((mx-x)*(mx-x)+(my-y)*(my-y)).real)
	mt=int(juli/30)
	return mx,my
# def move_t():
# 	global x,y,xj, yj
# 	if int(x)==int(mx) and int(y)==int(my):
# 		random_m()
# 	else:
# 		if x>mx:
# 			x=x-1
# 		else:
# 			x=x+1
# 		if y>my:
# 			y=y-1
# 		else:
# 			y=y+1


random_m()
def update(ind):
	global frame_s,mt
	global x,y,xj, yj
	if mt==0:
		random_m()
	mt=mt-1
	bx=int(tx/juli*mt)
	by=int(ty/juli*mt)
	if x>mx:
		x=x-bx-1
	elif x<mx:
		x=x+bx+1
	if y>my:
		y=y-by-1
	elif y<my:
		y=y+by+1
	if x>1440 or x<0 or y>960or y<0:
		x,y=random_m()
		root.wm_attributes("-topmost", True)  # 始终置顶层
	m="+{}+{}".format(x,y)
	root.geometry(m)  # 设置窗口位置或大小
	if (ind == framenum-1):#
		ind = 0
	frame = frames[ind]
	ind += 1
	date=str(datetime.datetime.now())[:19]
	fg='#dddddd'
	if " 18:3" in date:
		date=date+"  下班回家"
		fg='#FF0000'
		mytext = get_replicate_text(date)
	elif  " 10:4" in date:
		date=date+"  休息，休息10分钟,喝杯水"
		fg='#00FF00'
		pass
	elif  " 11:4" in date:
		date=date+"  休息，休息10分钟,上个洗手间"
		fg='#00FF00'
		pass
	elif  " 14:3" in date:
		date=date+"  休息，休息10分钟,喝杯水"
		fg='#00FF00'
		pass
	elif  " 15:3" in date:
		date=date+"  休息，休息10分钟在战3小时"
		fg='#00FF00'
		pass
	elif  " 16:3" in date:
		date=date+"  休息，休息10分钟在战2小时"
		fg='#00FF00'
		pass
	elif  " 17:3" in date:
		date=date+"  休息，休息10分钟在战1小时 ,喝杯水"
		fg='#00FF00'
		pass
	else:
		fg = '#fdfdfd'
		date=date+"  .......working"
	if fg == '#fdfdfd':
		pass
		label.configure(image=frame)
	else:
		mytext = get_replicate_text(date)

		label.configure(image=frame,text=mytext,compound='left', font=('Times New Roman', '15'), fg=fg, bg='white')
		# label.configure(image=frame)
	root.after(frame_s, update, ind)
	# label = tkinter.Label(text=mytext, compound='left', font=('Times New Roman', '15'), fg='#999999', bg='white')
	# label.pack()  # 显示

label = tkinter.Label(root,bg='white')#设置白色为透明
label.pack() #显示
root.after(0, update, 0)
root.mainloop() #循环