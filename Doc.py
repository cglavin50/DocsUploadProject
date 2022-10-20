import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import os


class Doc:

    def __init__(self, title):
        root = Tk()
        root.title(title)
        root.geometry("1200x660")
        global opened_name
        opened_name = False  # initialized to false, will change if it has been saved

        # create a new file function (will later port this over to main interactable window!!
        def new_file():
            txtBox.delete("1.0", END)  # first line is 1.0, END refers to last line in a tkinter textbox
            root.title('New Text Document')
            status_bar.config(text="New File        ")

            global opened_name
            opened_name = False  # initialized to false, will change if it has been saved

        # end new file temp

        # open files, again port over later
        def open_file():
            # clear out previous text
            txtBox.delete("1.0", END)  # first line is 1.0, END refers to last line in a tkinter textbox

            # grab filename
            cwd = os.getcwd()
            text_file = filedialog.askopenfilename(initialdir=cwd, title="Open File", filetypes=(
            ("Text Files", "*.txt"), ("JSON Files", "*.json"), ("Python Files", "*.py"),
            ("All Files", "*.*")))  # location of where you want to save the files, hard code for now

            if text_file:
                global opened_name  # make this global for save (seeing if this is an opened document)
                opened_name = text_file

            # update status bars
            name = text_file
            temp = cwd.replace("\\", '/') + "/"
            status_bar.config(text=f'{name}        ')
            # name = "*" + name.replace(temp, "")  # from video, replaces initial location with an empty string, replace doesn't modify actual string though
            # I want to implement a * icon, however this will come later
            name = name.replace(temp, "")
            root.title(f'{name}')

            # open the file
            if text_file: # now doesn't crash if clicking cancel, however title and statusbar is still wrong
                text_file = open(text_file, 'r')  # open file in read mode
                body = text_file.read()  # extract all the information

                txtBox.insert(END, body)  # after clearing text box, add new information

                # close file after getting info
                text_file.close()

        # end open_file

        # save as file
        def save_as_file():
            cwd = os.getcwd()
            text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=cwd, title="Save File",
                                                     filetypes=(("Text Files", "*.txt"), ("JSON Files", "*.json"),
                                                                ("Python Files", "*.py"), ("All Files", "*.*")))
            if text_file:  # meaning we didn't exit the menu
                # update status bars
                name = text_file
                status_bar.config(text=f'Saved: {name}        ')
                temp = cwd.replace("\\", '/') + "/"
                name = name.replace(temp, "")
                root.title(f'{name}')  # .title is a function to rename

                # save the file
                text_file = open(text_file, 'w')
                text_file.write(txtBox.get(1.0, END))  # get everything from line 1 to END

                # update opened name
                global opened_name
                opened_name = text_file  # update name if we change it in save as

                text_file.close()


            # end if

        # end save as

        # Save file
        def save_file():
            # need to discern if the file has been saved before, if not, do save as
            global opened_name  # get global variable, don't use local

            if opened_name:
                text_file = open(opened_name, 'w')  # open the file with writing capabilities
                text_file.write(txtBox.get(1.0, END))  # fill opened_name with our textbox

                text_file.close()
                #could put status update/popup box here

                status_bar.config(text=f'Saved: {opened_name}        ')
            # end save file
            else:
                save_as_file()
            # end else

        # end save_file

        # create master frame
        fr = Frame(root)
        fr.pack(pady=5)

        # create scroll bar for txt box
        text_scroll = Scrollbar(fr)
        text_scroll.pack(side=RIGHT, fill=Y)

        # create text box
        txtBox = Text(fr, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow",
                      selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
        txtBox.pack()

        # configure scrollbar
        text_scroll.config(command=txtBox.yview)

        # create menu
        my_menu = Menu(root)
        root.config(menu=my_menu)

        # add file menu
        file_menu = Menu(my_menu, tearoff=False)  # insert it to my menu
        my_menu.add_cascade(label="File", menu=file_menu)
        # file_menu.add_command(label="New", command=new_file)
        file_menu.add_command(label="New", command=lambda: new_file())
        # file_menu.add_command(label="Open", command=open_file)
        file_menu.add_command(label="Open", command=lambda: open_file())
        file_menu.add_command(label="Save", command=lambda: save_file())
        file_menu.add_command(label="Save As", command=lambda: save_as_file())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # add edit menu
        edit_menu = Menu(my_menu, tearoff=False)  # insert it to my menu
        my_menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")

        # add status bar to bottom of window
        status_bar = Label(root, text="Ready        ", anchor=E)
        status_bar.pack(fill=X, side=BOTTOM, ipady=5)  # internally pads within window, fills entirely horizontally

        root.mainloop()
    # end constructor
