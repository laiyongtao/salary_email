# coding:utf-8
import tkinter as tk

'''紧耦合'''


# 弹窗
class PopupDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('设置用户信息')

        self.parent = parent  # 显式地保留父窗口

        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
        tk.Label(row1)
        self.name = tk.StringVar()
        tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)
        tk.Label(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
        self.age = tk.IntVar()
        tk.Entry(row2, textvariable=self.age, width=20).pack(side=tk.LEFT)

        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        # 显式地更改父窗口参数
        self.parent.name = self.name.get()
        self.parent.age = self.age.get()

        # 显式地更新父窗口界面
        self.parent.l1.config(text=self.parent.name)
        self.parent.l2.config(text=self.parent.age)

        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()


# 主窗
class MyApp(tk.Tk):

    def __init__(self):
        super().__init__()
        # self.pack() # 若继承 tk.Frame，此句必须有！！！
        self.title('用户信息')

        # 程序参数
        self.name = '张三'
        self.age = 30

        # 程序界面
        self.setupUI()

    def setupUI(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
        self.l1 = tk.Label(row1, text=self.name, width=20)
        self.l1.pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
        self.l2 = tk.Label(row2, text=self.age, width=20)
        self.l2.pack(side=tk.LEFT)

        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="设置", command=self.setup_config).pack(side=tk.RIGHT)

    # 设置参数
    def setup_config(self):
        pw = PopupDialog(self)
        self.wait_window(pw)  # 这一句很重要！！！

        return


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()