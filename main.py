#!/usr/bin/python3.5
#File name: main.py
#Author: Luke Morrow
#Date Created: 7/16/2018
#Python Version: 3.5

import sys
import os
import tkinter as tk
import include.controller as controller

if __name__ == "__main__":
    controller = controller.Controller()
    if len(sys.argv) == 2:
        dir = sys.argv[1]
        if os.path.isdir(dir):
            controller.setDirectory(dir)
        else:
            print(dir + "is not a directory")
            sys.exit(1)
    tk.mainloop()
