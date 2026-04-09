from tkinter import *
from tkinter import ttk
import tkinter as tk

import report as report
import setup as setup
import tests as tests
import installer as installer

import multiprocessing

LABEL_COL:int = 0
ENTRY_COL:int = 1
BUTTON_COL:int = 20


def main():
    multiprocessing.freeze_support()
    setup.readSens()

    root = Tk()
    root.geometry("1000x400")

    installer.update(root)

    bodyFRM = ttk.Frame(root, padding=10)
    bodyFRM.grid()

    bodyFRM.master.title("Selenium WebTester")

    urlFRM = ttk.Frame(bodyFRM, padding=5, width=100,height=100,borderwidth=10, relief=tk.GROOVE)
    urlFRM.grid(row = 0, column = 0)
    urlChange(urlFRM)

    runFRM = ttk.Frame(bodyFRM, padding=5, borderwidth=10, relief=tk.GROOVE)
    runFRM.grid(row = 10, column = 10)
    runButtons(runFRM,root)

    root.mainloop()

def openFileExplorer():
    import webbrowser
    webbrowser.open(f"{setup.sensitive["PATH"]}/reports")

def runButtons(runFRM,root):
    ttk.Button(runFRM, text="Run", command=report.run).grid(column=BUTTON_COL, row=10)
    ttk.Button(runFRM, text="Open", command=openFileExplorer).grid(column=BUTTON_COL, row=11)
    ttk.Button(runFRM, text="Quit", command=root.destroy).grid(column=BUTTON_COL, row=12)

def urlChange(frm):
    
    ttk.Label(frm, text="Current URL").grid(column=LABEL_COL, row = 0)

    global currentURL
    currentURL = tk.StringVar()    
    currentURL.set(setup.sensitive["LINK"])
    ttk.Label(frm, textvariable=currentURL).grid(column=LABEL_COL+1, row = 0)
    ttk.Label(frm, text=f"New URL").grid(column=LABEL_COL, row = 2)

    global newURL
    newURL = tk.StringVar()
    ttk.Entry(frm, textvariable=newURL).grid(column=ENTRY_COL, row =2)

    ttk.Button(frm, text="Update URL", command=updateURL).grid(column=ENTRY_COL, row=3)

def updateURL():
    url = newURL.get()
    setup.setLink(url)
    currentURL.set(url)
    newURL.set("")

if __name__ == "__main__":
    main()