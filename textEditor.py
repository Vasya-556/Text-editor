from tkinter import *
from tkinter import ttk

def New_file():
    ...
    
def Open_file():
    ...
    
def Save_file():
    ...
    
def Save_as_file():
    ...

def Help_window():
    helpWindow = Toplevel(root)
 
    helpWindow.title("Help")
 
    helpWindow.geometry("200x200")
 
    # Label(helpWindow, 
    #       text ="This is a new window").pack()

def toggle_wrap():
    if wrap_var.get():
        text.config(wrap='word')
    else:
        text.config(wrap='none')

root = Tk()
root.title("Text Editor")
root.geometry("600x300")

frm = ttk.Frame(root, padding=3)
frm.grid(sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=New_file)
filemenu.add_command(label="Open", command=Open_file)
filemenu.add_command(label="Save", command=Save_file)
filemenu.add_command(label="Save as", command=Save_as_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=Help_window)

wrap_var = BooleanVar()
wrap_var.set(True)

helpmenu.add_checkbutton(label="Wrap button", onvalue=True, offvalue=False, variable=wrap_var, command=toggle_wrap)
menubar.add_cascade(label="Help", menu=helpmenu)

text = Text(frm, height = 5, width = 52, wrap='word')
text.grid(column=0, row=0,sticky=(N, S, E, W))

scrollbar = Scrollbar(frm, command=text.yview)
scrollbar.grid(column=1,row=0, sticky=(N, S, E, W))

text.config(yscrollcommand=scrollbar.set)

root.config(menu=menubar)
root.mainloop()