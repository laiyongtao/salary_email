import threading
import datetime
import base64

import tkinter as tk
from email.mime.text import MIMEText
from email.utils import formataddr

from tkinter import ttk
from .db_instance import set_db, SalaryEmail
from .setting_box import AccountPasswordWin, SMTPPortWin, InfoWin, SysSettingWin
from .parse_execl import ParseExcel
import tkinter.messagebox
import tkinter.filedialog

from smtplib import SMTP_SSL, SMTP
from decimal import (Decimal)

DEFAULT_COUNT = 4

class MainWin(tk.Tk):

    def __init__(self):
        super(MainWin, self).__init__()
        self.title('Salary E-mail Main')
        self.geometry('600x600')
        self.resizable(width=False, height=False)  # 禁制拉伸大小
        self.label_width = 55  # 标签长度

        self.db = set_db()
        self.subject = tk.StringVar() # 邮件标题
        self.salary_file_path = tk.StringVar()
        self.send_date = tk.StringVar() # 发件时间
        self.sender_text = tk.StringVar()
        self.sender_name_text = tk.StringVar()
        self.sign_text = tk.StringVar()
        self.smtp_text = tk.StringVar()
        self.port_text = tk.StringVar()
        self.__password = tk.StringVar()

        self.done_count = 0  # 完成的邮件数量
        self.P_count = tk.IntVar()  # 进度条量
        self.lock = threading.Lock()  # 计数增量线程锁
        self.gen_lock = threading.Lock()  # 行数据生成器线程锁

        self.thread_count = tk.IntVar() # 发送邮件进程数

        self.show_percent = tk.StringVar()  # 显示百分百
        self.show_percent.set('完成百分比：0%')

        self.show_percent_th = threading.Thread(target=self.show_percent_run)

        self.excel_file = None
        self.setupUI()
        self.set_default_info()

    def setupUI(self):
        '''主界面'''

        # 设置菜单栏
        menubar = self.set_menubar()
        self.config(menu=menubar)
        self.show_base_info()

    def show_account_box(self):
        account_box = AccountPasswordWin(parent=self)
        self.wait_window(account_box)

    def show_smtp_port_box(self):
        smtp_box = SMTPPortWin(parent=self)
        self.wait_window(smtp_box)

    def show_info_box(self):
        info_box = InfoWin(parent=self)
        self.wait_window(info_box)

    def set_menubar(self):
        '''菜单栏'''
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="文件", menu=filemenu)

        filemenu.add_command(label='退出', command=self.quit)
        settingmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="设置", menu=settingmenu)
        settingmenu.add_command(label="账号/密码", command=self.show_account_box)
        settingmenu.add_command(label="SMTP域名/端口", command=self.show_smtp_port_box)
        settingmenu.add_command(label="邮件信息设置", command=self.show_info_box)
        settingmenu.add_command(label="系统设置", command=self.show_sys_setting_box)
        return menubar

    def show_sys_setting_box(self):
        '''显示系统设置菜单'''
        sys_setting_box = SysSettingWin(parent=self)
        self.wait_window(sys_setting_box)

    def show_base_info(self):
        '''显示基本信息'''

        row1 = tk.Frame(self)
        row1.pack(fill='x', padx=1, pady=5)
        tk.Label(row1, text="发件邮箱：", width=15).pack(side=tk.LEFT)
        tk.Label(row1, textvariable=self.sender_text, width=self.label_width).pack(side=tk.LEFT)
        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text="发件人：", width=15).pack(side=tk.LEFT)
        tk.Label(row2, textvariable=self.sender_name_text, width=self.label_width).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill='x', padx=1, pady=5)
        tk.Label(row3, text="邮件标题：", width=15).pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self.subject, width=self.label_width, justify=tk.CENTER).pack(side=tk.LEFT)

        row5 = tk.Frame(self)
        row5.pack(fill='x', padx=1, pady=5)
        tk.Label(row5, text="邮件签名/落款：", width=15).pack(side=tk.LEFT)
        tk.Label(row5, textvariable=self.sign_text, width=self.label_width).pack(side=tk.LEFT)

        row6 = tk.Frame(self)
        row6.pack(fill='x', padx=1, pady=5)
        tk.Label(row6, text="邮件日期：", width=15).pack(side=tk.LEFT)
        tk.Entry(row6, textvariable=self.send_date, width=self.label_width, justify=tk.CENTER).pack(side=tk.LEFT)

        row7 = tk.Frame(self)
        row7.pack(fill='x', padx=1, pady=5)
        tk.Label(row7, text="SMTP服务器：", width=15).pack(side=tk.LEFT)
        tk.Label(row7, textvariable=self.smtp_text, width=30, justify=tk.CENTER).pack(side=tk.LEFT)
        tk.Label(row7, text="PORT：", width=10).pack(side=tk.LEFT)
        tk.Label(row7, textvariable=self.port_text, width=10, justify=tk.CENTER).pack(side=tk.LEFT)

        row4 = tk.Frame(self)
        row4.pack(fill='x', padx=1, pady=5)
        tk.Label(row4, text="工资条文件：", width=15).pack(side=tk.LEFT)
        tk.Entry(row4, textvariable=self.salary_file_path, width=self.label_width, justify=tk.CENTER).pack(side=tk.LEFT)
        tk.Button(row4, text='Open', command=self.get_salary_file_path, width=5).pack(side=tk.LEFT)

        tk.Button(self, command=self.send_email, text='发送', width=20).pack(padx=1, pady=5)
        tk.Label(self, textvariable=self.show_percent ).pack(padx=1, pady=5)

        # 进度条
        row8 = tk.Frame(self, padx=20, pady=1)
        row8.pack(fill='x', padx=1, pady=5)
        self.progressbar = ttk.Progressbar(row8, orient='horizontal', length=545, mode="determinate", variable=self.P_count)
        self.progressbar.pack(side=tk.LEFT)



        # 发送结果显示框
        self.result_box = tk.Frame(self, borderwidth=1, padx=20, pady=0)
        self.result_box.pack(fill='x',padx=1, pady=5)
        self.result_list = ttk.Treeview(self.result_box, height=10, show="headings")
        self.result_list['columns'] = ('姓名', "邮箱", '发送结果')
        self.result_list.column('姓名', width=120, anchor=tk.CENTER)  # 表示列,不显示
        self.result_list.column("邮箱", width=300, anchor=tk.CENTER)
        self.result_list.column('发送结果', width=120, anchor=tk.CENTER)
        self.result_list.heading('姓名', text="姓名")
        self.result_list.heading("邮箱", text="邮箱")
        self.result_list.heading('发送结果', text='发送结果')
        self.result_list.grid(row=0, column=0, sticky=tk.NSEW)
        vbar = ttk.Scrollbar(self.result_box, orient=tk.VERTICAL, command=self.result_list.yview)
        self.result_list.configure(yscrollcommand=vbar.set)
        vbar.grid(row=0, column=1, sticky=tk.NS)

    def count_done_row(self):
        '''计算完成的任务数'''
        with self.lock:
            self.done_count += 1
            self.P_count.set(self.done_count)

    def show_percent_run(self):
        total_count = self.excel_file.nrows
        current_count = self.done_count
        percent = "%0.1f" % (current_count/float(total_count) * 100)
        self.show_percent.set("完成百分百：{}%".format(percent))

    def get_salary_file_path(self):
        '''获取工资条文件路径'''
        path = tk.filedialog.askopenfilename(title='选择文件', filetypes=[("Excel File", "*.xls *.xlsx")])
        self.salary_file_path.set(path)

    def set_default_info(self):
        '''设置默认初始值'''
        self.subject.set('{}年{}月工资明细'.format(*self._get_year_month()))
        try:
            sender = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender').first()
            sender_text = sender.field_value if sender else ""
            sender_name = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender_name').first()
            sender_name_text = sender_name.field_value if sender_name else ""
            sign = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sign').first()
            sign_text = sign.field_value if sign else ""
            smtp = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='smtp_server').first()
            smtp_text = smtp.field_value if smtp else ""
            port = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='port').first()
            port_text = port.field_value if port else ""
            thread = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='thread_count').first()
            thread_count = int(thread.field_value) if thread else DEFAULT_COUNT

        except Exception as e:
            tk.messagebox.showerror(title='错误', message='数据库错误！\n{}'.format(e))
            sender_text = ''
            sender_name_text = ''
            sign_text = ''
            smtp_text = ''
            port_text = ''
            thread_count = DEFAULT_COUNT
        self.sender_text.set(sender_text)
        self.sender_name_text.set(sender_name_text)
        self.sign_text.set(sign_text)
        self.send_date.set(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.smtp_text.set(smtp_text)
        self.port_text.set(port_text)
        self.thread_count.set(thread_count)

    def send_email(self):
        '''发送邮件'''
        try:
            file_name = self.salary_file_path.get()
            if file_name.rsplit('.', 1)[1].lower() not in ('xlsx', 'xls'):
                tk.messagebox.showerror(title='文件错误', message='请选择正确的excel文件！')
                return
            self.excel_file = ParseExcel(file_name=file_name)
            # 初始化进度条
            self.progressbar['maximum'] = self.excel_file.nrows
            self.P_count.set(0)
        except Exception as e:
            tk.messagebox.showerror(title='文件错误', message='请选择正确的excel文件！\n{}'.format(e))
            return
        try:
            password = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name == 'password').first()
            self.__password.set(base64.decodebytes(password.field_value).decode('utf-8'))
        except Exception as e:
            tk.messagebox.showerror(title='错误', message='数据库错误！\n{}'.format(e))
            return

        self.done_count = 0  # 重置计数
        gen = self.excel_file.iter_salary_line()
        thread_count = self.thread_count.get() or DEFAULT_COUNT
        for i in range(thread_count):
            print(i)
            send_thread = threading.Thread(target=self._send_email, args=(gen, self.gen_lock))  # 子线程发送邮件
            send_thread.setDaemon(True)
            send_thread.start()

    def _send_email(self, gen, gen_lock):
        ob = SendEmail(self, self.__password.get(), gen, gen_lock)
        ob.run()

    @staticmethod
    def _get_year_month():
        today = datetime.datetime.now()
        year = today.year
        month = today.month
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        return year, month


class SendEmail(object):

    def __init__(self, win, password, gen, gen_lock):
        self.win = win
        self.__password = password
        self.gen = gen  # excel文件的生成器
        self.gen_lock = gen_lock

    def send_email(self):
        # 起线程发送邮件，设置发送百分百显示
        try:
            smtp = self._login_smpt()  # 登陆邮箱
        except Exception as e:
            return

        sender_text = self.win.sender_text.get()
        sender_name_text = self.win.sender_name_text.get()
        sign_text = self.win.sign_text.get()
        date = self.win.send_date.get()

        while True:
            try:
                with self.gen_lock:
                    row = next(self.gen)
            except StopIteration:
                break
            flag = True
            try:
                self._send_email(smtp=smtp, sender=sender_text, sender_name=sender_name_text, sign=sign_text, date=date, info_row=row)
            except Exception as e:
                try:
                    self._send_email(smtp=smtp, sender=sender_text, sender_name=sender_name_text, sign=sign_text,
                                     date=date, info_row=row)
                except Exception as e:
                    flag = False
                else:
                    pass
            else:
                pass
            self.win.count_done_row()
            self.win.show_percent_run()
            self.win.result_list.insert('', 'end', values=(row[0][1], row[-1][1], "成功！" if flag else "发送失败！！！"))


    def _send_email(self, smtp, sender, sender_name, sign, date, info_row):

        msg = self._make_mail_text(sender=sender, sender_name=sender_name, sign=sign, date=date,
                                   info_row=info_row)
        smtp.sendmail(from_addr=sender, to_addrs=[info_row[-1][1]], msg=msg)


    def _login_smpt(self):
        '''登陆邮箱'''
        try:
            sender_text = self.win.sender_text.get()
            smtp_server = self.win.smtp_text.get()
            port = int(self.win.port_text.get())

            password = self.__password
            port = int(port)
        except Exception as e:
            tk.messagebox.showerror(title='错误', message='数据库错误！\n{}'.format(e))
            return

        try:
            if port == 25:
                smtp = SMTP(host=smtp_server, port=port)
            elif port == 465:
                smtp = SMTP_SSL(host=smtp_server, port=port)
            else:
                raise ConnectionError('SMTP 端口错误')
            smtp.login(sender_text, password)
        except Exception as e:
            tk.messagebox.showerror(title='登陆错误', message='请检查账号信息是否正确！\n{}'.format(e))
            raise

        return smtp

    def _make_mail_text(self, sender, sender_name, sign, date, info_row):
        mail_text = '''
            <html>
            <body>
            <style type="text/css">
        			.info{
        				text-align: center;
        			}
        			.info tr th{
        				padding: 2px 10px;
        			}
        		</style>
        		<table class="info" border="1">
        		    <caption>%s</caption>
        			<tr>
        	''' % self.win.subject.get()

        for h in info_row[:-1]:
            mail_text += "<th>%s</th>" % str(h[0]).strip()

        mail_text += "</tr><tr>"

        for l in info_row[:-1]:
            l = str(l[1]).strip()
            if l == "":
                l = "0.00"
            try:
                l = Decimal(l).quantize(Decimal('.01'))
            except Exception:
                pass
            l = str(l)
            mail_text += "<td>%s</td>" % l

        mail_text += '''
                    </tr>
                </table>
                <div>
        			<p>%s<p>
        			<p>%s</p>
        		</div>
        		</body></html>
            ''' % (sign, date)

        msg = MIMEText(mail_text, 'html', 'utf-8')
        msg['From'] = formataddr([sender_name, sender])
        msg['To'] = formataddr([info_row[0][1].strip(), info_row[-1][1].strip()])
        msg['Subject'] = self.win.subject.get()
        return msg.as_string()

    def run(self):
        self.send_email()




if __name__ == '__main__':
    win = MainWin()
    win.mainloop()
