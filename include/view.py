#File name: view.py
#Author: Luke Morrow
#Date Created: 7/16/2018
#Python Version: 3.6

import sys, os
import tkinter as tk
from tkinter import messagebox
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
        #Add root tkinter
        root = tk.Tk()
        root.bind("<Escape>", sys.exit)
        root.title("Luke's Super Duper Dupe Finder")
        root.geometry(GEOMETRY)
        self.controller = controller
        self.dir = tk.StringVar()
        #create frame to house buttons
        buttonFrame = tk.Frame(root)
        buttonFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#0000FF')
        buttonFrame.pack(side=tk.TOP, fill=tk.BOTH)
        #create label for entry prompt
        self.label = tk.Label(buttonFrame, text="Enter a path to search:")
        self.label.pack(side=tk.LEFT)
        #create entry box
        self.entry = tk.Entry(buttonFrame, textvariable=self.dir, width=40)
        self.entry.bind("<Return>", lambda event: self.findDupes())
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.config(relief=tk.SUNKEN, bd=5)
        self.entry.focus()
        #create reset button linked to clearText command
        reset = tk.Button(buttonFrame, text="Reset", command=self.clearText)
        reset.pack(side=tk.LEFT, anchor=tk.W)
        reset.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg="#ff0000")
        #create find button linked to findDupes command
        find = tk.Button(buttonFrame, text="Find Dupes", command=self.findDupes)
        find.pack(side=tk.LEFT, anchor=tk.W)
        find.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg="#ff0000")
        #create quit button linked to sys.exit command
        quit = tk.Button(buttonFrame, text="Quit", command=sys.exit)
        quit.pack(side=tk.RIGHT, anchor=tk.E)
        quit.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg="#ff0000")
        #create results frame to house list boxes
        resultFrame = tk.Frame(root)
        resultFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#00ff00')
        resultFrame.pack(side=tk.BOTTOM)
        scrollbar = tk.Scrollbar(resultFrame)
        scrollbar.pack( side = tk.RIGHT, fill=tk.Y )
        #since there are two file locations for each duplicate files, we will use two listboxes
        self.results = tk.Listbox(resultFrame, yscrollcommand = scrollbar.set)
        self.results.pack( side = tk.LEFT, fill = tk.BOTH )
        self.results.config( bg='white', bd=5)
        self.results.config(width=WIDTH//2, height=HEIGHT)

        self.results2 = tk.Listbox(resultFrame, yscrollcommand = scrollbar.set)
        self.results2.pack( side = tk.LEFT, fill = tk.BOTH )
        self.results2.config( bg='white', bd=5)
        self.results2.config(width=WIDTH//2, height=HEIGHT)

        scrollbar.config( command = self.syncScroll )

    #this function will find duplicate files by the controller calling the model's find dupes function
    def findDupes(self):
        if self.results.get(0, tk.END) != None:
            self.results.delete(0, tk.END)
            self.results2.delete(0, tk.END)
        #if the user has not entered an alternative path use cwd
        if self.entry.get() == "":
            print(os.getcwd())
            dupes=self.controller.findDupes(os.getcwd())
            for x in dupes:
                self.results.insert(tk.END, x[0])
                self.results2.insert(tk.END, x[1])
        else:
            #ensure the path is a valid directory before searching
            if os.path.isdir(self.entry.get()):
                dupes=self.controller.findDupes(self.entry.get())
                for x in dupes:
                    self.results.insert(tk.END, x)
                    self.results2.insert(tk.END, x[1])
            else:
                messagebox.showinfo("Incorrect Path", "Oops, that isn't a valid path!")

    def clearText(self):
        self.results.delete(0, tk.END)
        self.results2.delete(0, tk.END)
        self.dir.set("")
        self.entry.focus()

    def syncScroll(self, *args):
        apply(self.results.yview(*args))
        apply(self.results2.yview(*args))
