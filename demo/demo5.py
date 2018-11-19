from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.geometry("800x600")

tv = ttk.Treeview(root, height=10, columns=('c1', 'c2', 'c3'))
for i in range(1000):
    tv.insert('', i, values=('a' + str(i), 'b' + str(i), 'c' + str(i)))
tv.pack()

# ----vertical scrollbar------------
vbar = ttk.Scrollbar(root, orient=VERTICAL, command=tv.yview)
tv.configure(yscrollcommand=vbar.set)
tv.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=0, column=1, sticky=NS)

# ----horizontal scrollbar----------
hbar = ttk.Scrollbar(root, orient=HORIZONTAL, command=tv.xview)
tv.configure(xscrollcommand=hbar.set)
hbar.grid(row=1, column=0, sticky=EW)
root.mainloop()