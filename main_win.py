
import tkinter as tk
from db_instance import set_db, SalaryEmail
from setting_box import AccountPasswordWin
import tkinter.messagebox
# from salary_email.db_instance import SalaryEmail

class MainWin(tk.Tk):

    def __init__(self):
        super(MainWin, self).__init__()
        self.title('Salary E-mail Main')
        self.geometry('600x400')
        self.setupUI()
        self.db = set_db()

    def setupUI(self):
        '''主界面'''

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="文件", menu=filemenu)

        filemenu.add_command(label='退出', command=self.quit)
        settingmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="设置", menu=settingmenu)
        settingmenu.add_command(label="账号/密码", command=self.show_account_box)
        settingmenu.add_command(label="SMTP域名/端口")
        self.config(menu=menubar)

    def show_account_box(self):
        account_box = AccountPasswordWin(parent=self)
        self.wait_window(account_box)

if __name__ == '__main__':
    win = MainWin()
    win.mainloop()
