from tkinter import *

import sys

system = sys.platform
if 'w' in system:
    root = Tk()  # 生成主窗口
    root.geometry('300x300')  # 改变窗体大小（‘宽x高’）
    root.title('hello')  # 窗口名字
    root.geometry('+960+300')  # 改变窗体位置（‘+横坐标+纵坐标’）
    root.resizable(True, True)  # 将窗口大小设置为可变/不可变
    e = Entry(root)
    e.grid(padx=100, pady=20)#pack-包装 grid-网格 place-位置
    e.delete(0, END)
    e.insert(0, '默认文本...')
    Button(root, text='芝麻开门', width=10, command=show) \
 \
        .grid(row=3, column=0, sticky=W, padx=10, pady=5)
    Button(root, text='点击退出', width=10, command=root.quit).grid(padx=100,pady=200)
    root.mainloop()
