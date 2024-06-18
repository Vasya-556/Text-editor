from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os

selected_file = None
file_saved = True

def New_file(event=None):
    global file_saved
    if file_saved:
        text.delete('1.0','end')
    else:
        Save_window(handle_save_on_new_file)
    
def handle_save_on_new_file(result):
    global file_saved
    if result == 'file saved' or result == 'file not saved':
        text.delete('1.0','end')
        file_saved = True
    
def handle_save_on_quit(result):
    global file_saved
    if result == 'file saved' or result == 'file not saved':
        file_saved = True
        root.quit()

def Save_window(callback):
    save_window = Toplevel(root)
    save_window.title("Save")
    save_window.geometry("300x150+500+300")
    
    label = Label(save_window, text="Do you want to save changes?", pady=20)
    label.pack()
    
    def save():
        Save_file()
        callback('file saved')
        save_window.destroy()
    
    def dont_save():
        callback('file not saved')
        save_window.destroy()
    
    def cancel():
        callback('canceled')
        save_window.destroy()
    
    button_one = Button(save_window, text="Save", command=save)
    button_one.pack(side=LEFT, padx=20)
    
    button_two = Button(save_window, text="Don't save", command=dont_save)
    button_two.pack(side=LEFT, padx=20)
    
    button_three = Button(save_window, text="Cancel", command=cancel)
    button_three.pack(side=LEFT, padx=20)

def Open_file(event=None):
    global selected_file
    global file_saved
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
        file_saved = True
        root.title(f'{os.path.basename(file.name)} - TextEditor' )
    
def Save_file(event=None):
    global selected_file
    global file_saved
    if selected_file is not None:  
        with open(selected_file, 'w') as file:
            file.write(text.get('1.0', 'end-1c'))
        file_saved = True
    else: 
        Save_as_file()
    
def Save_as_file(event=None):
    global selected_file
    global file_saved
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file = fd.asksaveasfile(filetypes=filetypes, defaultextension='.txt')
    
    if file is not None:  
        selected_file = file.name
        with open(selected_file, 'w') as f:
            f.write(text.get('1.0', 'end-1c'))
        file_saved = True

def Help_window(event=None):
    helpWindow = Toplevel(root)
 
    helpWindow.title("Help")
 
    helpWindow.geometry("200x200")
 
    # Label(helpWindow, 
    #       text ="This is a new window").pack()

def toggle_wrap(event=None):
    if event is None:
        if wrap_var.get():
            text.config(wrap='word')
            vertical_scrollbar.grid_remove()
        else:
            text.config(wrap='none')
            vertical_scrollbar.grid()
    else:
        wrap_var.set(not wrap_var.get())
        toggle_wrap()

def text_edited(e):
    global file_saved
    if e.state & 0x4 and e.keycode == 78:  
        New_file(e)  
        return
    if e.state & 0x4 and e.keycode == 83:  
        if e.state & 0x1:  
            Save_as_file(e)
        else:
            Save_file(e) 
        return
    if e.state & 0x4 and e.keycode == 79:  
        Open_file(e)  
        return
    if e.state & 0x4 and e.keycode == 81:  
        quit(e)  
        return
    if e.state & 0x4 and e.keycode == 72:  
        Help_window(e)  
        return
    if e.state & 0x4 and e.keycode == 87:  
        toggle_wrap(e)  
        return
    if e.state & 0x4 and e.keycode == 90:  
        Undo(e)  
        return
    if e.state & 0x4 and e.keycode == 89:  
        Redo(e)  
        return
    if e.state & 0x4 and e.keycode == 70:  
        Find_text(e)  
        return
    file_saved = False

def Undo(event=None):
    try:
        text.edit_undo()  
    except TclError:
        pass

def Redo(event=None):
    try:
        text.edit_redo()  
    except TclError:
        pass    

def quit(event=None):
    global file_saved
    if file_saved:
        root.destroy()
    else:
        Save_window(handle_save_on_quit)

def cut_text(event=None):
    text.event_generate('<Control-x>')

def copy_text(event=None):
    text.event_generate('<Control-c>')

def paste_text(event=None):
    text.event_generate('<Control-v>')

def Find_text(event=None):
    search_window = Toplevel(root)
    
    search_window.title("Search")
 
    search_window.geometry("260x100")

    search_label = Label(search_window, text="Enter text to search:")
    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = Entry(search_window)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    def search():
        text_to_search = search_entry.get()
        if text_to_search:
            start_pos = '1.0'
            while True:
                start_pos = text.search(text_to_search, start_pos, stopindex='end', nocase=1, regexp=False)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(text_to_search)}c"
                text.tag_add('search', start_pos, end_pos)
                start_pos = end_pos
            text.tag_config('search', background="yellow", foreground="black")

    def clear_highlight():
        search_entry.delete(0, 'end')
        text.tag_remove("search", "1.0", END)  
    
    def close_search_window():
        clear_highlight()
        search_window.destroy()

    search_button = Button(search_window, command=search, text='Search')
    search_button.grid(row=1,column=0, padx=5, pady=5)

    clear_button = Button(search_window, command=clear_highlight, text='Clear')
    clear_button.grid(row=1,column=1, padx=5, pady=5)
    
    search_entry.focus_set()
    search_window.resizable(False, False)
    search_window.protocol("WM_DELETE_WINDOW", close_search_window)

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
filemenu.add_command(label="New", command=New_file, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=Open_file, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=Save_file, accelerator="Ctrl+S")
filemenu.add_command(label="Save as", command=Save_as_file, accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit, accelerator="Ctrl+Q")
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='Undo', command=Undo, accelerator="Ctrl+Z")
editmenu.add_command(label='Redo', command=Redo, accelerator="Ctrl+Y")
editmenu.add_command(label='Cut', command=cut_text, accelerator="Ctrl+X")
editmenu.add_command(label='Copy', command=copy_text, accelerator="Ctrl+C")
editmenu.add_command(label='Paste', command=paste_text, accelerator="Ctrl+V")
editmenu.add_command(label='Find', command=Find_text, accelerator="Ctrl+F")
menubar.add_cascade(label='Edit', menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=Help_window, accelerator="Ctrl+H")

wrap_var = BooleanVar()
wrap_var.set(True)

helpmenu.add_checkbutton(label="Wrap words", onvalue=True, offvalue=False, variable=wrap_var, command=toggle_wrap, accelerator="Ctrl+W")
menubar.add_cascade(label="Help", menu=helpmenu)

text = Text(frm, height = 5, width = 52, wrap='word', undo=True)
text.grid(column=0, row=0,sticky=(N, S, E, W))
text.bind('<Key>',text_edited)

scrollbar = Scrollbar(frm, command=text.yview)
scrollbar.grid(column=1,row=0, sticky=(N, S, E, W))

vertical_scrollbar = Scrollbar(frm,orient='horizontal', command=text.xview)
vertical_scrollbar.grid(column=0,row=1,sticky=(N, S, E, W))
vertical_scrollbar.grid_remove()

text.config(yscrollcommand=scrollbar.set)
text.config(xscrollcommand=vertical_scrollbar.set)

root.protocol("WM_DELETE_WINDOW", quit)

root.config(menu=menubar)
root.mainloop()