# !/usr/bin/python3
from tkinter import *
import statistics as stats
from tkinter import messagebox
import tkinter
import os
import re
import numpy as np
import pandas as pd
from tkinter import ttk
from tkinter.filedialog import askdirectory


data_structure = {}
df_train = None
df_test = None
path = ""
lower = {}
upper = {}


#  --------------------------------------  This function activate when the user press "Browse"
def setLocation():
    global path
    temp_path = askdirectory()

    path = temp_path
    tf_directoryPath.config(state='normal')
    tf_directoryPath.insert(0, path)
    tf_directoryPath.config(state='disabled')

    if len(path)>0:
        btn_Build.config(state='normal')


#  --------------------------------------  This function activate when the user press "Build"
def trainModel():
    global df_train
    global data_structure
    global path

    df_train = None
    data_structure = {}

    train_file_path = path + "/train.csv"
    structure_file_path = path + "/Structure.txt"

    try:
        num_of_bins = int(tf_DiscretizationBins.get())
        if num_of_bins < 0:
            messagebox.showerror("Naive Bayes Classifier","Negative integer, please enter a positive integer")
            return
    except ValueError:
        messagebox.showerror("Naive Bayes Classifier", "Please enter a positive integer")
        return

    if (os.path.exists(structure_file_path) == False):
        messagebox.showerror("Naive Bayes Classifier", "Structure.txt file was not found in directory:" + path)
        return
    if (os.path.exists(train_file_path) == False):
        messagebox.showerror("Naive Bayes Classifier", "train.csv file was not found in directory:" + path)
        return

    data_structure = loadStructure(structure_file_path)
    df_train = prepareData(train_file_path, num_of_bins)

    messagebox.showinfo("Naive Bayes Classifier", "Building classifier using train - set is done!")
    btn_Classify.config(state='normal')


def loadStructure(structure_file_path):
    file = open(structure_file_path, 'r')
    data_structure = {}

    for line in file:
        attributes = re.search('^@ATTRIBUTE\s+(.+?)\s+(.*?)\s*$', line)
        attribute_name = attributes.group(1)
        if (attributes.group(2)[0] == '{' and attributes.group(2)[-1] == '}'):
            data_structure[attribute_name] = attributes.group(2)[1:-1].split(',')
        else:
            data_structure[attribute_name] = attributes.group(2)

    return data_structure


def prepareData(data_path, num_of_bins):
    global lower
    global upper
    df = pd.read_csv(data_path)

    for key in data_structure.keys():
        data = data_structure[key]
        df[key].replace('', np.nan, inplace=True)

        if (data == 'NUMERIC'):
            li = list(pd.unique(df[key]))
            n = len(li)
            if n == 3 and df[key].isnull().values.any():
                must_common = stats.mode(df[key])
                df[key].replace(np.nan, must_common, inplace=True)
            else:
                # if there is nan value - full it with the mean value of the column according to the class
                key_mean_value = df.pivot_table(key, columns='class', aggfunc='mean')
                for classification in data_structure['class']:
                    df.loc[(df['class'] == classification) & (np.isnan(df[key])), key] = key_mean_value[classification][key]

                if (df_train is None):
                    lower[key] = min(df[key])
                    upper[key] = max(df[key])

                li = list(pd.unique(df[key]))
                n = len(li)
                if n > num_of_bins:
                    equalWidth(num_of_bins, df, key)

        # else if the attribute is categorical
        else:
            must_common = stats.mode(df[key])
            df[key].replace(np.nan, must_common, inplace=True)

    return df


def equalWidth(num_of_bins, df, attribute):
    global lower
    global upper

    ew = float(upper[attribute] - lower[attribute]) / num_of_bins
    bins_range = []
    p_inf = float("inf")
    n_inf = float("-inf")

    bins_range.append(n_inf)
    for i in range(1, num_of_bins):
        bins_range.append((i * ew) + lower[attribute])
    bins_range.append(p_inf)

    for i in range((len(bins_range) - 1)):
        df.loc[(df[attribute] > bins_range[i]) & (df[attribute] <= bins_range[i + 1]), attribute] = (i + 1)


#  --------------------------------------  This function activate when the user press "Classify"
def runPredict():
    global df_test
    global num_of_bins
    global path
    try:
        num_of_bins = int(tf_DiscretizationBins.get())
        if num_of_bins < 0:
            messagebox.showerror("Naive Bayes Classifier", "Negative integer, please enter a positive integer")
            return
    except ValueError:
        messagebox.showerror("Naive Bayes Classifier", "Please enter a positive integer")
        return

    test_file_path = path + "/test.csv"

    if (os.path.exists(test_file_path) == False):
        messagebox.showerror("Naive Bayes Classifier", "test.csv file has not found in directory:" + path)
        return

    df_test = prepareData(test_file_path, num_of_bins)
    result = NaiveBayesClassifier(df_test)
    writeResult(result)
    messagebox.showinfo("Naive Bayes Classifier",
                        "Classification finished.\n You can view the result in " + path + "/output.txt")

    root.quit()

def NaiveBayesClassifier(df_test_param):
    global df_train
    global data_structure

    result = []
    m = 2;
    class_count = {}
    class_probability = {}
    for classification in data_structure['class']:
        class_count[classification] = len(df_train.loc[(df_train['class'] == classification), 'class'])
        class_probability[classification] = class_count[classification]/len(df_train['class'])

    for index, row in df_test_param.iterrows(): # for each data frame
        max_score = 0
        max_class = ""
        for classification in data_structure['class']:
            probability_attribute_givven_class = 1;
            n = class_count[classification]

            for attribute in data_structure.keys():
                if attribute != 'class':
                    if (data_structure[attribute] == 'NUMERIC'):
                        M = num_of_bins
                    else:
                        M = len(data_structure[attribute]) # how much different values in this attribute


                    nc = len(df_train.loc[(df_train['class'] == classification) & (
                                df_train[attribute] == row[attribute]), attribute])
                    probability_attribute_givven_class = probability_attribute_givven_class * (
                                float((nc + m * (1 / M))) / float((n + m)))


            if (max_score < float(probability_attribute_givven_class) * class_probability[classification]):
                max_score = float(probability_attribute_givven_class) * class_probability[classification]
                max_class = classification

        result.append(max_class)

    return result


def writeResult(result):
    with open(path + "/output.txt", "w") as file:
        for i in range(len(result)):
            file.write(str(i + 1) + " " + result[i] + "\n")




root = tkinter.Tk()
root.title('Naive Bayes Classifier')
root.geometry('450x220')
root.config(bg="white")

label1 = ttk.Label(root, text='Directory Path', background="white")
label1.place(x=20, y=30)
tf_directoryPath = ttk.Entry(root, width=50, state='disabled')
tf_directoryPath.place(x=20, y=50)

btn_borwseDirectoryPath = ttk.Button(root, text='Browse', command=setLocation)
btn_borwseDirectoryPath.place(x=350, y=47.5)

label2 = ttk.Label(root, text='Discretization Bins', background="white")
label2.place(x=20, y=100)

tf_DiscretizationBins = ttk.Entry(root, width=50)
tf_DiscretizationBins.place(x=20, y=120)
tf_DiscretizationBins.insert(0, "3")

btn_Build = ttk.Button(root, text='Build', command=trainModel, state='disabled')
btn_Build.place(x=150, y=170)

btn_Classify = ttk.Button(root, text='Classify', command=runPredict, state='disabled')
btn_Classify.place(x=250, y=170)

root.mainloop()
