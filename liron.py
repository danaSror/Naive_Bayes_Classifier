from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd
from PIL import Image, ImageTk

class liron:
    def __init__(self, master):
        # fields
        self.index = 0
        self.master = master
        master.title("Naïve Bayes Classifier")
        self.clusters = 0
        self.runs = 0
        self.filename = ""
        self.data = ""
        self.path = ""
        # creation of controllers
        self.filename_label = Label(master, textvariable=self.filename)
        self.clusters_label = Label(master, text="Number of clusters k:")
        self.runs_label = Label(master, text="Number of runs:")
        clusters_vcmd = master.register(self.validate_clusters) # we have to wrap the command
        runs_vcmd = master.register(self.validate_runs)  # we have to wrap the command
        self.clusters_entry = Entry(master, validate="key", validatecommand=(clusters_vcmd, '%P'))
        self.runs_entry = Entry(master, validate="key", validatecommand=(runs_vcmd, '%P'))
        self.Browse_button = Button(master, text="Browse", command=lambda: self.handle("Browse"))
        self.Pre_process_button = Button(master, text="Pre-process", command=lambda: self.handle("Pre-process"), state=DISABLED)
        self.Cluster_button = Button(master, text="Cluster", command=lambda: self.handle("Cluster"), state=DISABLED)

        # placement on controllers on the grid
        self.Browse_button.grid(row=self.index, column=0)
        self.index += 1
        self.filename_label.grid(row=self.index, column=0)
        self.index += 1
        self.Pre_process_button.grid(row=self.index, column=0)
        self.index += 1
        self.clusters_label.grid(row=self.index, column=0, sticky=W)
        self.index += 1
        self.clusters_entry.grid(row=self.index, column=0, columnspan=3, sticky=W + E)
        self.index += 1
        self.runs_label.grid(row=self.index, column=0, sticky=W)
        self.index += 1
        self.runs_entry.grid(row=self.index, column=0, columnspan=3, sticky=W + E)
        self.index += 1
        self.Cluster_button.grid(row=self.index, column=0, sticky=W+E)
        self.index += 1

    # this function checks the input field number of clusters and validates it
    def validate_clusters(self, new_text):
        if not new_text:  # the field is being cleared
            messagebox.showinfo("K Means Clustering", "please enter number of clusters")
            return False
        try:
            self.clusters = int(new_text)
            if self.clusters <= 0 or self.clusters > 164:
                messagebox.showinfo("K Means Clustering", "invalid number of clusters")
                return False
            return True
        except ValueError:
            messagebox.showinfo("K Means Clustering", "please enter numbers only")
            return False

    # this function checks the input field number of runs and validates it
    def validate_runs(self, new_text):
        if not new_text:  # the field is being cleared
            messagebox.showinfo("K Means Clustering", "please enter number of runs")
            return False
        try:
            self.runs = int(new_text)
            if self.runs <= 0:
                messagebox.showinfo("K Means Clustering", "invalid number of runs")
                return False
            return True
        except ValueError:
            messagebox.showinfo("K Means Clustering", "please enter numbers only")
            return False

    # this function handles on click actions from user
    def handle(self, method):
        if method == "Browse":
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
        elif method == "Pre-process":
            self.data = pre_process(self.filename)
            messagebox.showinfo("K Means Clustering", "Preprocessing completed successfully!")
            self.Cluster_button['state'] = 'normal'
        elif method == "Cluster":
            if self.runs <= 0 or self.clusters <= 0:
                messagebox.showinfo("K Means Clustering", "invalid input numbers")
            else:

                scatter_image = Image.open(self.path+'/scatter.png')
                scatter_plot_photo = ImageTk.PhotoImage(scatter_image)
                map_image = Image.open(self.path + '/map.png')
                map_photo = ImageTk.PhotoImage(map_image)
                lab1 = Label(image=scatter_plot_photo)
                lab1.image = scatter_plot_photo
                lab1.grid(row=self.index, column=0)
                lab2 = Label(root, image=map_photo)
                lab2.image = map_photo
                lab2.grid(row=self.index, column=1)


root = Tk()
my_gui = liron(root)
root.mainloop()
