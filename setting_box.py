# coding:utf-8
import re
import tkinter as tk
import base64
import tkinter.messagebox

from .db_instance import SalaryEmail


class AccountPasswordWin(tk.Toplevel):
    '''账号密码设置'''

    def __init__(self, parent):
        super(AccountPasswordWin, self).__init__()
        self.title('账户设置')
        self.geometry('300x120')
        self.attributes("-topmost", 1)  # 保持在前
        self.resizable(width=False, height=False)  # 禁制拉伸大小
        self.parent = parent
        self.db = parent.db
        self.setupUI()

    def setupUI(self):

        self.email_address = tk.StringVar()
        self.password = tk.StringVar()

        try:
            email_address = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name == 'sender').first()
            password = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name == 'password').first()
            if email_address:
                self.email_address.set(email_address.field_value)
            if password:
                self.password.set(base64.decodebytes(password.field_value).decode('utf-8'))
        except Exception as e:
            tk.messagebox.showerror(title="错误", message="数据库错误，请重试！\n{}".format(e))

        row1 = tk.Frame(self)
        row1.pack(fill='x', padx=1, pady=5)
        tk.Label(row1, text="发件邮箱：", width=15).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.email_address, width=25).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text='密码(授权码)：', width=15).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.password, width=25, show='*').pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill='x')
        tk.Button(row3, text='Cancel', command=self.cancel, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)
        tk.Button(row3, text='Save', command=self.saveBT, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)

    def saveBT(self):
        sender = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender').first()
        password = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='password').first()
        if not sender:
            sender = SalaryEmail()
            sender.field_name = 'sender'
            sender.memo = "发件人邮箱地址！"
        if not password:
            password = SalaryEmail()
            password.field_name= 'password'
            password.memo = "密码"
        # 验证邮箱格式
        sender_text = self.email_address.get()
        password_text = self.password.get()
        if len(password_text) > 0 and re.match(r'[0-9A-Za-z][\.-_0-9A-Za-z]*@[0-9A-Za-z]+(\.[0-9A-Za-z]+)+$', sender_text):
            sender.field_value = sender_text
            password.field_value = base64.encodebytes(password_text.encode('utf-8'))
            self.db.session.add_all([sender,password])
            self.db.session.commit()
            # 更新主窗口信息
            self.parent.sender_text.set(sender_text)
            tk.messagebox.showinfo(title='success', message='Save Successfully!')
            self.destroy()
        elif len(password_text) <= 0:
            tk.messagebox.showinfo(title='密码错误', message='密码不能为空!')
        elif not re.match(r'[0-9A-Za-z][\.-_0-9A-Za-z]*@[0-9A-Za-z]+(\.[0-9A-Za-z]+)+$', sender_text):
            tk.messagebox.showinfo(title='邮箱地址错误', message='请输入正确的邮箱地址!')

    def cancel(self):
        res = tk.messagebox.askyesno(title='是否取消设置？', message="设置的内容未保存，是否退出？")
        if res:
            self.destroy()


class SMTPPortWin(tk.Toplevel):
    '''smtp/port设置窗口'''

    def __init__(self, parent):
        super(SMTPPortWin, self).__init__()
        self.title('SMTP设置')
        self.geometry('300x120')
        self.attributes("-topmost", 1)  # 保持在前
        self.resizable(width=False, height=False)  # 禁制拉伸大小
        self.parent = parent
        self.db = parent.db
        self.setupUI()

    def setupUI(self):
        '''搭建界面'''
        self.smtp_server = tk.StringVar()
        self.port = tk.StringVar()
        try:
            smtp_server = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='smtp_server').first()
            port = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='port').first()
            if smtp_server:
                self.smtp_server.set(smtp_server.field_value)
            if port:
                self.port.set(port.field_value)
        except Exception as e:
            tk.messagebox.showerror(title="错误", message="数据库错误，请重试！\n{}".format(e))

        row1 = tk.Frame(self)
        row1.pack(fill='x', padx=1, pady=5)
        tk.Label(row1, text="SMTP服务器：", width=15).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.smtp_server, width=25).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text='SMTP端口：', width=15).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.port, width=25).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill='x')
        tk.Button(row3, text='Cancel', command=self.cancel, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)
        tk.Button(row3, text='Save', command=self.saveBT, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)

    def saveBT(self):
        smtp_server = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='smtp_server').first()
        port = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='port').first()
        if not smtp_server:
            smtp_server = SalaryEmail()
            smtp_server.field_name = 'smtp_server'
            smtp_server.memo = "SMTP服务器地址"
        if not port:
            port = SalaryEmail()
            port.field_name= 'port'
            port.memo = "SMTP端口"
        # 验证邮箱格式
        smtp_text = self.smtp_server.get()
        port_text = self.port.get()
        if len(smtp_text) and len(port_text):
            if str(port_text) not in ('25','465'):
                tk.messagebox.showinfo(title='端口错误', message='请输入正确的端口号25/465(ssl)!')
                return
            smtp_server.field_value = smtp_text
            port.field_value = port_text
            self.db.session.add_all([smtp_server,port])
            self.db.session.commit()
            self.parent.smtp_text.set(smtp_text)
            self.parent.port_text.set(port_text)
            tk.messagebox.showinfo(title='success', message='Save Successfully!')
            self.destroy()
        else:
            tk.messagebox.showinfo(title='输入错误', message='请输入正确的配置!')


    def cancel(self):
        res = tk.messagebox.askyesno(title='是否取消设置？', message="设置的内容未保存，是否退出？")
        if res:
            self.destroy()


class InfoWin(tk.Toplevel):
    '''邮件信息设置'''

    def __init__(self, parent):
        super(InfoWin, self).__init__()
        self.parent = parent
        self.db = parent.db
        self.geometry('300x120')
        self.attributes("-topmost", 1)  # 保持在前
        self.resizable(width=False, height=False)  # 禁制拉伸大小
        self.setupUI()

    def setupUI(self):
        '''界面搭建'''
        self.sender_name = tk.StringVar()
        self.sign = tk.StringVar()
        try:
            sender_name = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender_name').first()
            sign = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sign').first()
            if sender_name:
                self.sender_name.set(sender_name.field_value)
            if sign:
                self.sign.set(sign.field_value)
        except Exception as e:
            tk.messagebox.showerror(title="错误", message="数据库错误，请重试！\n{}".format(e))

        row1 = tk.Frame(self)
        row1.pack(fill='x', padx=1, pady=5)
        tk.Label(row1, text="发件人：", width=15).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.sender_name, width=25).pack(side=tk.LEFT)

        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text='签名/落款：', width=15).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.sign, width=25).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill='x')
        tk.Button(row3, text='Cancel', command=self.cancel, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)
        tk.Button(row3, text='Save', command=self.saveBT, padx=10, pady=2, width=8).pack(side=tk.RIGHT, padx=10, pady=2)

    def saveBT(self):
        sender_name = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name == 'sender_name').first()
        sign = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name == 'sign').first()
        if not sender_name:
            sender_name = SalaryEmail()
            sender_name.field_name = 'sender_name'
            sender_name.memo = "发件人"
        if not sign:
            sign = SalaryEmail()
            sign.field_name = 'sign'
            sign.memo = "邮件落款"
        # 验证邮箱格式
        sender_name_text = self.sender_name.get()
        sign_text = self.sign.get()
        if len(sender_name_text) and len(sign_text):
            sender_name.field_value = sender_name_text
            sign.field_value = sign_text
            self.db.session.add_all([sender_name, sign])
            self.db.session.commit()
            # 更新主窗口信息
            self.parent.sender_name_text.set(sender_name_text)
            self.parent.sign_text.set(sign_text)
            tk.messagebox.showinfo(title='success', message='Save Successfully!')
            self.destroy()
        else:
            tk.messagebox.showinfo(title='输入错误', message='请输入正确的配置!')

    def cancel(self):
        res = tk.messagebox.askyesno(title='是否取消设置？', message="设置的内容未保存，是否退出？")
        if res:
            self.destroy()

if __name__ == '__main__':
    pass



