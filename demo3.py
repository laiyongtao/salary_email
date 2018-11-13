from tkinter import *

root = Tk()
mbYes, mbYesNo, mbYesNoCancel, mbYesNoAbort = 0, 1, 2, 4


# 定义一个消息对话框，依据传入的参数不同，弹出不同的提示信息
def MessageBox():  # 没有使用使用参数
    mbType = mbYesNo
    textShow = 'Yes'
    if mbType == mbYes:
        textShow = 'Yes'
    elif mbType == mbYesNo:
        textShow = 'YesNo'
    elif mbType == mbYesNoCancel:
        textShow = 'YesNoCancel'
    elif mbType == mbYesNoAbort:
        textShow = 'YesNoAbort'
    tl = Toplevel(height=200, width=400)
    Label(tl, text=textShow).pack()


# 由Button来启动这个消息框，因为它使用了空的回调函数，故MessageBox改为了无参数形式，使用了固定
# 值mbYesNo
Button(root, text='click me', command=MessageBox).pack()
root.mainloop()