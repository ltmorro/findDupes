#File name: view.py
#Author: Luke Morrow
#Date Created: 7/16/2018
#Python Version: 3.6

import sys, os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import include.model as model

GEOMETRY = '1280x720+200+10'
WIDTH = 146
HEIGHT = 19
class Controller(object):
    def __init__(self):
        pass

    def findDupes(self, dir):
        print("Sending path: " + dir + "to model to find dupes.")

class View(object):
    def __init__(self, controller):
        self.backgroundColor = "#b2bec3"
        self.buttonColor = "#0984e3"
        self.buttonHoverColor = "#74b9ff"
        self.cautionColor = "#d63031"
        self.cautionHoverColor = "#ff7675"
        self.listColor = "#dfe6e9"
        # self.buttonFonn
        #Add root tkinter
        root = tk.Tk()
        root.bind("<Escape>", sys.exit)
        root.title("Luke's Super Duper Dupe Finder")
        self.controller = controller
        self.dir = tk.StringVar()
        self.dir.set(os.getcwd())
        #create frame to house buttons
        buttonFrame = tk.Frame(root)
        buttonFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.backgroundColor)
        buttonFrame.pack(side=tk.TOP, fill=tk.X)
        #create button for browsing directories
        browse = tk.Button(buttonFrame, text="Browse", command=self.chooseDir)
        browse.pack(side=tk.LEFT, anchor=tk.W)
        browse.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.buttonColor, activebackground=self.buttonHoverColor)
        #create label for entry prompt
        self.label = tk.Label(buttonFrame, text=" or enter a path to search:")
        self.label.pack(side=tk.LEFT)
        self.label.config(padx=5, pady=5)
        #create entry box
        self.entry = tk.Entry(buttonFrame, textvariable=self.dir, width=40)
        self.entry.bind("<Return>", lambda event: self.findDupes())
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.config(relief=tk.SUNKEN, bd=5)
        self.entry.focus()
        #create reset button linked to clearText command
        reset = tk.Button(buttonFrame, text="Reset", command=self.clearText)
        reset.pack(side=tk.LEFT, anchor=tk.W)
        reset.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.cautionColor, activebackground=self.cautionHoverColor)
        #create find button linked to findDupes command
        find = tk.Button(buttonFrame, text="Find Dupes", command=self.findDupes)
        find.pack(side=tk.LEFT, anchor=tk.W)
        find.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.buttonColor, activebackground=self.buttonHoverColor)
        #create quit button linked to sys.exit command
        quit = tk.Button(buttonFrame, text="Quit", command=sys.exit)
        quit.pack(side=tk.RIGHT, anchor=tk.E)
        quit.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.cautionColor, activebackground=self.cautionHoverColor)
        #create results frame to house list boxes
        resultFrame = tk.Frame(root)
        resultFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg=self.backgroundColor)
        resultFrame.pack(side=tk.TOP, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(resultFrame)
        scrollbar.pack( side = tk.RIGHT, fill=tk.Y )
        #since there are two file locations for each duplicate files, we will use two listboxes
        self.results = tk.Listbox(resultFrame, yscrollcommand = scrollbar.set)
        self.results.pack( side = tk.LEFT, fill = tk.BOTH, expand=1)
        self.results.config( bg=self.listColor, bd=5)
        # self.results.config(width=resultFrame.winfo_width()//2, height=resultFrame.winfo_height())

        self.results2 = tk.Listbox(resultFrame, yscrollcommand = scrollbar.set)
        self.results2.pack( side = tk.LEFT, fill = tk.BOTH, expand=1)
        self.results2.config( bg=self.listColor, bd=5)
        # self.results2.config(width=resultFrame.winfo_width()//2, height=resultFrame.winfo_height())

        scrollbar.config( command = self.syncScroll )

    #this function will find duplicate files by the controller calling the model's find dupes function
    def findDupes(self):
        if self.results.get(0, tk.END) != None:
            self.results.delete(0, tk.END)
            self.results2.delete(0, tk.END)
        #if the user has not entered an alternative path use cwd
        if self.dir.get() == os.getcwd():
            print(os.getcwd())
            dupes=self.controller.findDupes(os.getcwd())
            for x in dupes:
                self.results.insert(tk.END, x[0])
                self.results2.insert(tk.END, x[1])
        else:
            #ensure the path is a valid directory before searching
            if os.path.isdir(self.dir.get()):
                dupes=self.controller.findDupes(self.dir.get())
                for x in dupes:
                    self.results.insert(tk.END, x[0])
                    self.results2.insert(tk.END, x[1])
            else:
                messagebox.showinfo("Incorrect Path", "Oops, that isn't a valid path!")

    def clearText(self):
        self.results.delete(0, tk.END)
        self.results2.delete(0, tk.END)
        self.dir.set("")
        self.entry.focus()

    def syncScroll(self, *args):
        self.results.yview(*args)
        self.results2.yview(*args)

    def chooseDir(self):
        self.dir.set(filedialog.askdirectory())
