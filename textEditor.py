from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Text Editor")
root.geometry("600x300")

frm = ttk.Frame(root, padding=3)
frm.grid(sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)

text = Text(frm, height = 5, width = 52, wrap='word')
text.grid(column=0, row=0,sticky=(N, S, E, W))

scrollbar = Scrollbar(frm, command=text.yview)
scrollbar.grid(column=1,row=0, sticky=(N, S, E, W))

text.config(yscrollcommand=scrollbar.set)

root.mainloop()