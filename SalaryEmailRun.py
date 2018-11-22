# coding:utf-8
import os
import sys
# BASE_DIR = os.path.dirname(os.path.abspath(__name__))
# sys.path.insert(0, BASE_DIR)

from salary_mail.main_win import MainWin

window = MainWin()

if __name__ == '__main__':
    window.mainloop()