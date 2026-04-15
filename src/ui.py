from tkinter import *
from tkinter import ttk
import tkinter as tk

import report as report
import setup as setup
import tests as tests
import installer as installer

import multiprocessing
import logging
import datetime

LABEL_COL:int = 0
ENTRY_COL:int = 1
BUTTON_COL:int = 20


logger = logging.getLogger(__name__)

def main():
    multiprocessing.freeze_support()
    setup.readSens()

    time = datetime.datetime.today().strftime("%Y-%m-%d_%I-%M-%S_%p")
    fileName =f"logs/log_{time}.log"
    logging.basicConfig(filename=fileName, level=logging.INFO)
    logger.info("Main Started")

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
    logger.info("Opening Reports")
    webbrowser.open(f"{setup.sensitive["PATH"]}/reports")

def runButtons(runFRM,root):
    logger.info("Run Buttons GUI Stated ")
    ttk.Button(runFRM, text="Run", command=report.run).grid(column=BUTTON_COL, row=10)
    ttk.Button(runFRM, text="Open", command=openFileExplorer).grid(column=BUTTON_COL, row=11)
    ttk.Button(runFRM, text="Quit", command=root.destroy).grid(column=BUTTON_COL, row=12)

def urlChange(frm):
    logger.info("URL GUI Started")
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
    logger.info(f"Updating url: {currentURL} -> {newURL.get()}")
    url = newURL.get()
    setup.setLink(url)
    currentURL.set(url)
    newURL.set("")

def updatePrompt(root):
    if(installer.needUpdate()):
        logger.info("Update Needed")

        updateWindow = tk.Toplevel(root)
        updateWindow.geometry("400x100")
        updateWindow.title("Update Prompt")
        updateWindow.grid()
        updateWindow.attributes('-topmost', True)
        updateUI(updateWindow,root)

def restartNotification(root):
    logger.info("Restart Prompt Activated")

    restartWindow = tk.Toplevel(root)
    restartWindow.geometry("400x100")
    restartWindow.title("Restart Prompt")
    restartWindow.attributes('-topmost', True)
    restartWindow.grid()

    tk.Label(restartWindow, text="You will need to restart the program to get use the update").grid(column=3, row = 1)
    tk.Button(restartWindow, text="Quit", command=root.destroy).grid(column=6, row=2)

def updateUI(frm,root):
    logger.info("Update Prompt Activated")
    tk.Label(frm, text="Would you like to Update the Program?").grid(column=3, row = 1)
    tk.Button(frm, text="Yes", command= lambda: installer.downloadUpdate(frm,root)).grid(column=3, row=2)
    tk.Button(frm, text="No", command=frm.destroy).grid(column=6, row=2)

if __name__ == "__main__":
    main()