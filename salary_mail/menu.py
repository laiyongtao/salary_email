# coding:utf-8
import tkinter as tk
from .setting_box import AccountPasswordWin

def create_box(db):
    AccountPasswordWin(db)

def create_menubar(win):

    menubar = tk.Menu(win)

    filemenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="文件", menu=filemenu)

    filemenu.add_command(label='退出', command=win.quit)

    settingmenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="设置", menu=settingmenu)
    settingmenu.add_command(label="账号/密码")
    settingmenu.add_command(label="SMTP域名/端口")


    return menubar