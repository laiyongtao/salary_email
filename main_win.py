
import tkinter as tk
import datetime
from db_instance import set_db, SalaryEmail
from setting_box import AccountPasswordWin, SMTPPortWin, InfoWin
import tkinter.messagebox
import tkinter.filedialog

class MainWin(tk.Tk):

    def __init__(self):
        super(MainWin, self).__init__()
        self.title('Salary E-mail Main')
        self.geometry('600x400')
        self.db = set_db()
        self.subject = tk.StringVar() # 邮件标题
        self.salary_file_path = tk.StringVar()

        self.setupUI()

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
        return menubar

    def show_base_info(self):
        '''显示基本信息'''
        try:
            sender = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender').first()
            sender_text = sender.field_value if sender else ""
            sender_name = self.db.session.query(SalaryEmail).filter(SalaryEmail.field_name=='sender_name').first()
            sender_name_text = sender_name.field_value if sender_name else ""

        except Exception as e:
            tk.messagebox.showerror(title='错误', message='数据库错误！\n{}'.format(e))
            sender_text = ''
            sender_name_text = ''
        row1 = tk.Frame(self)
        row1.pack(fill='x', padx=1, pady=5)
        tk.Label(row1, text="发件邮箱：", width=15).pack(side=tk.LEFT)
        tk.Label(row1, text=sender_text, width=25).pack(side=tk.LEFT)
        row2 = tk.Frame(self)
        row2.pack(fill='x', padx=1, pady=5)
        tk.Label(row2, text="发件人：", width=15).pack(side=tk.LEFT)
        tk.Label(row2, text=sender_name_text, width=25).pack(side=tk.LEFT)

        self.set_default_subject()
        row3 = tk.Frame(self)
        row3.pack(fill='x', padx=1, pady=5)
        tk.Label(row3, text="邮件标题：", width=15).pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self.subject, width=25, justify=tk.CENTER).pack(side=tk.LEFT)

        row4 = tk.Frame(self)
        row4.pack(fill='x', padx=1, pady=5)
        tk.Label(row4, text="工资条文件：", width=15).pack(side=tk.LEFT)
        tk.Entry(row4, textvariable=self.salary_file_path, width=25, justify=tk.CENTER).pack(side=tk.LEFT)
        tk.Button(row4, text='Open', command=self.get_salary_file_path, width=5).pack(side=tk.LEFT)

    def get_salary_file_path(self):
        '''获取工资条文件路径'''
        path = tk.filedialog.askopenfilename(title='选择文件', filetypes=[("Excel File", "*.xls *.xlsx")])
        self.salary_file_path.set(path)

    def set_default_subject(self):
        '''发件标题'''
        self.subject.set('{}年{}月工资明细'.format(*self._get_year_month()))

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

if __name__ == '__main__':
    win = MainWin()
    win.mainloop()
