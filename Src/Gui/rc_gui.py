#!/usr/bin/python3
# imports: std
import traceback
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from typing import TypeVar
import hashlib

# imports: non-std

# imports: local
# from ...Src.rc_logger import logger

# const/globals
# log = logger()
T = TypeVar("T")

class PwgenApp:
    def __init__(self, *args,  master=None, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.cache = self.load_data()
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.title("Password Generator")
        toplevel1.resizable(False, False)
        toplevel1.report_callback_exception = self.show_error

        # Entry Frame
        entry_frame = ttk.Frame(toplevel1)
        entry_frame.configure(height=200, width=200)

        self.primary_key_var = tk.StringVar()
        primary_key_entry = ttk.Entry(entry_frame, textvariable=self.primary_key_var)
        primary_key_entry.bind("<Return>", lambda event: self.button_1())
        primary_key_entry.grid(column=1, padx="0 6", pady=6, row=0)

        button1 = ttk.Button(entry_frame, command=lambda: self.button_1())
        button1.configure(text='Generate')
        button1.grid(column=2, padx=6, pady=6, row=0)

        label1 = ttk.Label(entry_frame)
        label1.configure(text='Primary Password:')
        label1.grid(column=0, padx="6 0", pady=6, row=0)

        self.entry2_var = tk.StringVar()
        entry2 = ttk.Entry(entry_frame, textvariable=self.entry2_var)
        entry2.grid(column=1, padx="0 6", pady=6, row=1)

        button2 = ttk.Button(entry_frame, command=lambda: self.button_2())
        button2.configure(text='Add')
        button2.grid(column=2, padx=6, pady=6, row=1)

        label2 = ttk.Label(entry_frame)
        label2.configure(text='Account Website URL:')
        label2.grid(column=0, padx="6 0", pady=6, row=1)

        # Options Frame
        options_frame = ttk.Frame(entry_frame)
        options_frame.configure(height=200, width=200)

        label3 = ttk.Label(options_frame)
        label3.configure(
            text='Select an entry from the table then click on of the below buttons:')
        label3.grid(column=0, columnspan=3, padx=6, pady=6, row=0)

        button3 = ttk.Button(options_frame, command=lambda: self.button_3())
        button3.configure(text='Regenerate password')
        button3.grid(column=1, padx=6, pady="6 0", row=1)

        button4 = ttk.Button(options_frame, command=lambda: self.button_4())
        button4.configure(text='Delete Account Entry')
        button4.grid(column=2, padx=6, pady="6 0", row=1)

        button5 = ttk.Button(options_frame, command=lambda: self.button_5())
        button5.configure(text='Copy password to clipboard')
        button5.grid(column=0, padx=6, pady="6 0", row=1)

        options_frame.grid(
            column=0,
            columnspan=3,
            padx=6,
            pady="6 0",
            row=4,
            sticky="nsew")
        options_frame.rowconfigure("all", weight=1)
        options_frame.columnconfigure("all", weight=1)
        entry_frame.grid(column=0, row=0, sticky="nsew")

        # Treeview Frame

        treeview_frame = ttk.Frame(toplevel1)
        treeview_frame.configure(height=200, width=200)

        self.treeview1_var = tk.StringVar()
        self.treeview1 = ttk.Treeview(treeview_frame)
        self.treeview1.bind("<<TreeviewSelect>>", lambda event: self.treeview1_select(event))
        treeview1_cols = ['column1','column2']
        treeview1_dcols = ['column1','column2']
        self.treeview1.configure(selectmode="extended",columns=treeview1_cols,
            displaycolumns=treeview1_dcols,show='headings')
        self.treeview1.column(
            "column1",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.treeview1.column(
            "column2",
            anchor="w",
            stretch=True,
            width=200,
            minwidth=20)
        self.treeview1.heading("column1", anchor="w", text='Account Website URL')
        self.treeview1.heading("column2", anchor="w", text='Generated Password')
        self.treeview1.grid(column=0, padx="6 0", pady="6 0", row=0, sticky="nsew")

        scrollbar1 = ttk.Scrollbar(treeview_frame)
        scrollbar1.configure(orient="horizontal")
        scrollbar1.grid(column=0, padx="6 0", pady="0 6", row=1, sticky="new")

        scrollbar2 = ttk.Scrollbar(treeview_frame)
        scrollbar2.configure(orient="vertical")
        scrollbar2.grid(column=1, padx="0 6", pady="6 0", row=0, sticky="nsw")

        treeview_frame.grid(column=0, row=1, sticky="nsew")
        treeview_frame.rowconfigure(0, weight=1)
        treeview_frame.columnconfigure(0, weight=1)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def show_error(self, *args):
        # log.error(f"{args = }")
        error = traceback.format_exception(*args)
        messagebox.showerror("Exception", error)

    def treeview1_select(self, _event = None):
        for value in self.treeview1.selection():
            # print(self.treeview1.item(value)["values"])
            if len(self.treeview1.selection()) == 1:
                self.treeview1_var.set(self.treeview1.item(value)["values"][0])
                return self.treeview1_var.get()


    def button_1(self):
        # Generate Button
        primary_pw = self.primary_key_var.get()
        self.treeview1.delete(*self.treeview1.get_children())
        gen_hash = self.kwargs.get('generate', None)
        for hash_key in gen_hash(primary_pw):
            # print(hash_key)
            self.treeview1.insert(parent='', index=0, values=hash_key)
        pass

    def button_2(self):
        # Add Button
        url = self.entry2_var.get()
        add_entry = self.kwargs.get('add')
        if add_entry:
            add_entry(url)
        self.button_1()
        pass

    def button_3(self):
        # Regenerate password
        result = messagebox.askokcancel(title='Please Read',message='Are you sure?\nThere is no recovering password components.')
        if result:
            regen_pw = self.kwargs.get('regen')
            if regen_pw:
                regen_pw(self.treeview1_select())
            pass
        self.button_1()
        pass
    
    def button_4(self):
        # Delete account entry
        result = messagebox.askokcancel(title='Please Read',message='Are you sure?\nThere is no recovering deleted passwords.')
        if result:
            remove_pw = self.kwargs.get('remove')
            if remove_pw:
                remove_pw(self.treeview1_select())
            pass
        self.button_1()
        pass
    
    def button_5(self):
        # Copy password to clipboard
        for value in self.treeview1.selection():
            if len(self.treeview1.selection()) == 1:
                self.treeview1_var.set(self.treeview1.item(value)["values"][1])
                self.treeview1.clipboard_clear()
                self.treeview1.clipboard_append(self.treeview1_var.get())
        pass

    def load_data(self):
        pass



if __name__ == "__main__":
    app = PwgenApp()
    app.run()

