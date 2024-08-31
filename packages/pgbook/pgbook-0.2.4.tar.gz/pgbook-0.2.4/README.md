## Pygame Function Book

pygame be used easier

#### 1.下载 download

```shell
pip install pgbook
```

#### 2.简单的程序 easiest program

###### 1. esay

```python
from pgbook.screen.window import Window

mywindow = Window()
#窗口对象
mywindow.show()
#展示


'''
这段代码生成了一个空白窗口
'''
```

###### 2. window

```python
from pgbook.screen.window import Window

mywindow = Window()
#窗口对象
mywindow.set_name('Hello World')
#set_name:用于修改名称
mywindow.set_ico('logo.ico')
#set_ico:用于设置图标
mywindow.set_rect(0.4,0.4)
#set_rect:(w,h):
# w,h<=1 大小为屏幕大小的w,h倍
# w,h>1 大小为w,h
self.MaxFps = 60
#修改帧率
self.BlackGroungColor=(0,0,0)
#修改默认页面颜色

mywindow.show()
#展示


'''
这段代码展示了Window类的使用
'''
```

###### 3. 事件系统

```python
from pgbook.eventlist.thinglist import Thing,ThingList


t=Thing()
#单个事件对象

# 设置事件 方式1
def k(get1,get2):
    print(str(get1)+' and '+str(get2))
t.connect(k)

# 设置事件 方式2
@t.connect()
def k(get1,get2):
    print(str(get1)+' and '+str(get2))


t.set_name('PrintA')
#设置对象名称，用于寻找
t.did(256,None)
#输出：256 and None
#did:执行，传入参数
t.did_n(1024,False)
#输出：256 and False
#did_n:如果名称符合则执行，传入参数


t.lock()# 上锁did did_n不执行(也不报错)
t.lock(False)# 开锁 默认
t.lock()# 更改锁的方向


tl=ThingList()
# 事件列表，可叠多层

tl.set_name('PrintList')#检索名称
tl.lock(False)#锁功能同上，不执行本列表，但子对象不上锁


#添加事件 方式1
tl.connect(t)#Thing或ThingList均可，但不可传入自身，以防锁死
#添加事件 方式2
@tl.connect(name='PrintA')
def k(get1,get2):#注意保持参数统一
    print(str(get1)+' and '+str(get2))
#自动创建一个Thing对象，name为'PrintA'


tl.did('pan',64)#所有对象执行，同时受本身和子对象的锁影响
tl.did_n('apple',64)#名称正确对象执行

tl.lock_n('PrintA')
#给所有name='PrintA'的对象上锁
#不受tl.lock(True)的影响

tl.find_n('PrintA')
#返回第一个name='PrintA'的对象
#不受tl.lock(True)的影响

tl.find_n('PrintA').did(1,2)

'''
这段代码展示了事件系统的使用
'''
```

###### 4. Window中的事件

```python
from pgbook.screen.window import Window
import pygame

mywindow = Window()
#帧事件 mywindow.check
#实例
mywindow.MaxFps = 10
k=1
@mywindow.check.connect(name='TenTimesCheck')
def TTC(screen):#mywindow.check 有固定参数 screen
    global k
    k+=1
    if k==11:
        print('Check!')
        k=1
'''
大约每秒输出一次
'''

#事务 mywindow.event
#实例
@mywindow.event.connect(name='MouseDown')
def MD(event):#mywindow.event 有固定参数 event
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 获取鼠标点击的位置
        mouse_pos = pygame.mouse.get_pos()
        # 在控制台输出鼠标点击的位置
        print("鼠标点击位置:", mouse_pos)
'''
鼠标点击则输出
'''

mywindow.show()
```

###### 5. 控件

```python
from pgbook.object.object import Position

p=Position(x=10,y=25,max_x=989,max_y=74)#1600,1200的默认窗口
#默认使用百分比表示位置
print('p的百分比：('+str(p.x)+','+str(p.y)+')')
print('p的像素：('+str(p.true_pos().x)+','+str(p.true_pos().y)+')')

p=Position(x=100,y=250,max_x=989,max_y=74,use_percent_h=False,use_percent_t=True)
#使用千分比表示位置
print('p的千分比：('+str(p.x)+','+str(p.y)+')')
print('p的像素：('+str(p.true_pos().x)+','+str(p.true_pos().y)+')')

p=Position(x=20,y=50,max_x=989,max_y=74,use_percent_h=False,use_percent_t=False,percent=200)
#使用其他分制表示位置
print('p的两百分比：('+str(p.x)+','+str(p.y)+')')
print('p的像素：('+str(p.true_pos().x)+','+str(p.true_pos().y)+')')

p=Position(x=10,y=25,max_x=989,max_y=74)#1600,1200的默认窗口
#默认使用中心点表示位置
#x,y 的范围在 [-percent/2,percent/2]
#例如：默认在-50到50之间
try:
    p.set_pos(-51,0)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(-25,10)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(25,51)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(25,101)
except Exception as e:
    print('get error'+str(e))
p.show_pos()



p=Position(x=10,y=25,max_x=989,max_y=74,use_center=False)#1600,1200的默认窗口大小
#不使用中心点表示位置
#x,y 的范围在 [0,percent]
#例如：默认在0到100之间
try:
    p.set_pos(-51,0)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(-25,10)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(25,51)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
try:
    p.set_pos(25,101)
except Exception as e:
    print('get error'+str(e))
p.show_pos()
```

###### 6. 页面

页面用于管理大量控件的显示与隐藏，渲染该页面内容。

```python
from pgbook.screen.page import Page


p=Page()

# p.drawlist:ThingList f(screen)
# p.eventlist:ThingList f(event)

from pgbook.screen.window import Window
w = Window()

p.connect(w)#链接到窗口

w.show()

p.lock(True)#隐藏
p.lock(False)#显示
```

###### 7. 文字

```python
from pgbook.screen.window import Window
from pgbook.screen.page import Page
from pgbook.object.text import BaseText
w = Window()

p=Page()
p.connect(w)

t=BaseText(text='Some Text',color=(255,255,255),textsize=24,textfile=None)
t.new_data(text='你好',color=(128,128,128),textsize=36,textfile=None)

# text     :文字内容
# color    :文字颜色
# textsize :文字大小
# textfile :字体文件，None 使用默认字体

t.pos=p.set_pos(-40,-40)#文字位置

t.connect_page(p)

w.show()
```



###### 7.按钮

```python
from pgbook.screen.window import Window
from pgbook.screen.page import Page
from pgbook.object.button import TextButton
w = Window()

p=Page()
p.connect(w)

b=TextButton()
b.text.new_data(text='Some Text',color=(255,255,255),textsize=24,textfile=None)
b.pos.set_pos(-30,-30)

down_num=1

@b.drawlist.connect(name='ButtonDown')
def bd(screen):
    global down_num
    if b.Down.is_end():
        down_num+=1
        print(down_num)

w.show()
```

###### 8. 文本框

```python
from pgbook.screen.window import Window
from pgbook.screen.page import Page
from pgbook.object.text import EnglishTextInput

w=Window()

p=Page()
p.connect(w)

ti=EnglishTextInput()#同new_data
ti.connect_page(p)

ti.new_data(text='',#默认文字
empty_text='Input Some Text',#文本框为空时显示的文字
back_color=(138,138,138),#默认颜色（边框）
cback_color=(96,96,96),#选中改变的颜色（边框）
text_color=(255,255,255),#文字颜色
notext_color=(200,200,200),#文本框为空时显示的文字的颜色
centercolor=(168,168,168),#文本框背景颜色
textsize=24,#字体大小
textfile=None,#字体文件
width=256,#文本框宽度
outline=3)#文本框边框宽度

@ti.drawlist.connect(name='GetFocus')
def gf(screen):
    if b.IsFocus.is_true():
        print('获取焦点')
    if b.IsFocus.is_end():
        print('失去焦点')

ti.ShowFocus.len=50#光标闪烁速度 帧/次

w.show()
```

#### 3.版本记录

###### 0.1.x

1. 框架
2. 文本，按钮

###### 0.2.x

1. 文本框
