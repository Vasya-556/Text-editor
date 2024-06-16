from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

selected_file = None
file_saved = False

def New_file():
    global file_saved
    if file_saved:
        text.delete('1.0','end')
    else:
        Save_window()
    
def Save_window():
    save_window = Toplevel(root)
    save_window.title("Notepad")
    
    save_window.geometry("300x150+500+300")
    
    label = Label(save_window, text="Do you want to save changes?", pady=20)
    label.pack()

    def save():
        save_window.destroy()
    
    def dont_save():
        save_window.destroy()
    
    def cancel():
        save_window.destroy()
    
    button_one = Button(save_window, text="Save", command=save)
    button_one.pack(side=LEFT, padx=20)
    
    button_two = Button(save_window, text="Don't save", command=dont_save)
    button_two.pack(side=LEFT, padx=20)
    
    button_three = Button(save_window, text="Cancel", command=cancel)
    button_three.pack(side=LEFT, padx=20)

def Open_file():
    global selected_file
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    file = fd.askopenfile(filetypes=filetypes)
    
    if file is not None:  
        selected_file = file.name
        text.delete('1.0', 'end')  
        content = ''.join(file.readlines())
        text.insert('1.0', content)
    
def Save_file():
    global selected_file
    global file_saved
    if selected_file is not None:  
        with open(selected_file, 'w') as file:
            file.write(text.get('1.0', 'end-1c'))
        file_saved = True
    else: 
        Save_as_file()
    
def Save_as_file():
    global selected_file
    global file_saved
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file = fd.asksaveasfile(filetypes=filetypes, defaultextension='.txt')
    
    if file is not None:  
        selected_file = file.name
        file_saved = True

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

def text_edited(e):
    global file_saved
    file_saved = False

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
text.bind('<Key>',text_edited)

scrollbar = Scrollbar(frm, command=text.yview)
scrollbar.grid(column=1,row=0, sticky=(N, S, E, W))

text.config(yscrollcommand=scrollbar.set)

root.config(menu=menubar)
root.mainloop()