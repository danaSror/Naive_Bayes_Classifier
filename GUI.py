from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas as pd

class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Naïve Bayes Classifier")

        self.path = tk.StringVar()
        self.bins = tk.IntVar()

        self.path_label = tk.Label(root, text='Directory Path: ', font=('calibre', 10, 'bold'))
        self.path_entry = tk.Entry(root, textvariable=self.path, font=('calibre', 10, 'normal'))

        self.browse_btn = tk.Button(root, text='Browse', command=lambda: self.handle())
        self.build_btn = tk.Button(root, text='Build', command=lambda: self.handle())
        self.classify_btn = tk.Button(root, text='Classify', command=lambda: self.handle())

        self.bins_label = tk.Label(root, text='Discretization Bins: ', font=('calibre', 10, 'bold'))
        self.bins_entry = tk.Entry(root, textvariable=self.bins, font=('calibre', 10, 'normal'))

        self.path_label.grid(row=0, column=0)
        self.path_entry.grid(row=0, column=1)
        self.browse_btn.grid(row=0, column=2)
        self.bins_label.grid(row=2, column=0)
        self.bins_entry.grid(row=2, column=1)
        self.build_btn.grid(row=3, column=1)
        self.classify_btn.grid(row=4, column=1)


        # self.total = 0
        # self.entered_number = 0
        #
        # self.total_label_text = IntVar()
        # self.total_label_text.set(self.total)
        # self.total_label = Label(master, textvariable=self.total_label_text)
        #
        # self.label = Label(master, text="Directory Path:")
        # self.label2 = Label(master, text="Directory:")
        # self.entry2 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        #
        # vcmd = master.register(self.validate) # we have to wrap the command
        # self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        #
        # self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        # self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        # self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT

        # self.label.grid(row=0, column=0, sticky=W)
        # self.label2.grid(row=3, column=0, sticky=W)
        # self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        #
        # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        #
        # self.add_button.grid(row=2, column=0)
        # self.subtract_button.grid(row=2, column=1)
        # self.reset_button.grid(row=2, column=2, sticky=W+E)

    def handle(self):
        self.filename = askopenfilename()
        if not self.filename.endswith('.xlsx'): # valid xlsx file
            messagebox.showinfo("K Means Clustering", "invalid file")
        self.data = pd.read_excel(io=self.filename)
        if self.data.size == 0: # not empty
            messagebox.showinfo("K Means Clustering", "file is empty")
        else:
            split = self.filename.split("/")
            split.pop()
            self.path = '/'.join(split)
            self.filename_label['text'] = '' + self.filename
            self.Pre_process_button['state'] = 'normal'




root = Tk()
# setting the windows size
root.geometry("600x400")
my_gui = GUI(root)
root.mainloop()
