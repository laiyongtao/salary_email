# coding:utf-8
import tkinter as tk
from tkinter import mainloop
import tkinter.messagebox

from db_instance import SalaryEmail


class AccountPasswordWin(tk.Tk):
    '''账号密码设置'''

    def __init__(self, parent):
        super(AccountPasswordWin, self).__init__()
        self.title('账户设置')
        self.geometry('300x300')

        self.db = parent.db
        self.setupUI()

    def setupUI(self):
        row1 = tk.Frame(self)
        row1.pack(fill='x')
        tk.Label(row1, text="E-Mail Address：", width=15).pack(side=tk.LEFT)
        self.email_address = tk.StringVar()
        tk.Entry(row1, textvariable=self.email_address, width=20).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text='Password：', width=15).pack(side=tk.LEFT)
        self.password = tk.StringVar()
        tk.Entry(row2, textvariable=self.password, width=20).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill='x')
        tk.Button(row3, text='Save', command=self.saveAP, padx=5, pady=2).pack(side=tk.RIGHT)
        tk.Button(row3, text='Cancel', command=self.cancel, padx=5, pady=2).pack(side=tk.RIGHT)

    def saveAP(self):
        sender = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender').first()
        if not sender:
            sender = SalaryEmail()
        sender.field_name = 'sender'
        sender.field_value = self.email_address.get()
        self.db.session.add(sender)
        self.db.session.commit()
        tk.messagebox.showinfo(title='success', message='Save Successfully!')
        self.destroy()

    def cancel(self):
        self.destroy()

if __name__ == '__main__':
    class A(object):
        pass
    a = A()
    a.db = 1
    AccountPasswordWin(a)
    mainloop()



