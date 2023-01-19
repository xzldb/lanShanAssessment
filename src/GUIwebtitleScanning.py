import re
import urllib.request
from tkinter import *


def gettitle():
    url=e1.get()
    response = urllib.request.urlopen(url)
    html = response.read()
    html = html.decode()
    tag = re.search(r'<title>(.*?)</title>', html).group(0)
    tag = tag[:-8]
    tag = tag[7:]
    text.insert(INSERT, tag)
    root2.mainloop()


root = Tk()  # 生成主窗口
root.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root.title('欢迎使用webtitle搜索')  # 窗口名字
root.geometry('+960+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root.resizable(True, True)  # 将窗口大小设置为可变/不可变
la0 = Label(root, text='网址url').place(x=20,y=20)
img_gif = PhotoImage(file = 'img_gif.gif')
label_img = Label(root, image = img_gif).place(x=20,y=60)
# 第一个输入框位置功能
e1 = Entry(root)
e1.place(x=100, y=20)  # pack-包装 grid-网格 place-位置
e1.delete(0, END)  # 删除文本框里的值
e1.insert(0, '在这里输入url...')
# 两个按钮位置及功能
Button(root, text='开始查找', width=10, command=gettitle).place(x=10, y=250)
Button(root, text='点击退出', width=10, command=root.quit).place(x=200, y=250)
root2 = Tk()
root2.geometry('300x300')  # 改变窗体大小（‘宽x高’）
root2.title('结果窗口')  # 窗口名字
root2.geometry('+1260+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
root2.resizable(True, True)  # 将窗口大小设置为可变/不可变
text = Text(root2, width=50, height=30, undo=True, autoseparators=True)
text.pack()
root.mainloop()
