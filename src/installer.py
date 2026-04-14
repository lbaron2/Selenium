import requests
import setup as setup
import tkinter as tk
import os
import shutil

def update(root):
    setup.readSens()
    makeReqURL()
    global json
    json = requests.get(url).json()
    if(updatePrompt(root)):
        downloadUpdate()

def makeReqURL():
    setup.readSens()
    owner = setup.sensitive["OWNER"]
    repo = setup.sensitive["REPO"]
    global url
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

def getCurrentRelease() -> str:
    return json["name"]

def needUpdate() -> bool:
    localVersion = setup.sensitive["RELEASE"]

    remoteVersion = getCurrentRelease()

    if(localVersion != remoteVersion):
        return True
    return False

def updatePrompt(root):
    if(needUpdate()):
        updateWindow = tk.Toplevel(root)
        updateWindow.geometry("400x100")
        updateWindow.title("Do you want to Update")
        updateWindow.grid()
        updateUI(updateWindow)


def updateUI(frm):
    tk.Label(frm, text="Would you like to Update the Program?").grid(column=3, row = 1)
    tk.Button(frm, text="Yes", command=downloadUpdate).grid(column=3, row=2)
    tk.Button(frm, text="No", command=frm.destroy).grid(column=6, row=2)

def makeEXE():
    os.system(f"pyinstaller -y --clean --debug all -n WebTester -p {os.getcwd()}//src src/ui.py --onefile --distpath {os.getcwd()} --noconsole")
    # shutil.move("WebTester//WebTester.exe", "WebTester.exe")
    # shutil.move("WebTester//_internal", "_internal")

def downloadUpdate():
    zip_url = json['zipball_url']
    r = requests.get(zip_url, allow_redirects=True)
    with open('release.zip', 'wb') as f:
        f.write(r.content)
    makeEXE()
    setup.sensitive["RELEASE"] = json["name"] 
    setup.saveSens()

if __name__ == "__main__":
    makeEXE()