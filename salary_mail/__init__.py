# coding:utf-8
import tkinter as tk
import sqlite3
from .db_instance import set_db
from .menu import create_menubar
from .setting_box import AccountPasswordWin


def create_win():
    '''主进程'''
    win = tk.Tk()
    win.title('Salary E-mail Main')
    win.geometry('600x400')

    # 设置数据库

    win.db = set_db()
    # win.db = db
    # 设置菜单
    menu_bar = create_menubar(win)
    win.config(menu=menu_bar)
    ac = AccountPasswordWin(win.db)
    win.wait_window(ac)

    return win
