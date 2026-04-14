import requests
import setup as setup
import tkinter as tk
import os
import shutil
import zipfile
import ui

def update(root):
    setup.readSens()
    makeReqURL()
    global json
    json = requests.get(url).json()
    ui.updatePrompt(root)

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

def makeEXE():
    os.system(f"pyinstaller -y --clean --debug all -n WebTester -p {os.getcwd()}//src src/ui.py --onefile --distpath {os.getcwd()} --noconsole")


def getZip():
    zip_url = json['zipball_url']
    r = requests.get(zip_url, allow_redirects=True)
    with open('release.zip', 'wb') as f:
        f.write(r.content)

def updateFromZip():
    with zipfile.ZipFile('release.zip', 'r') as zip_ref:
        zip_ref.extractall("src")

    os.chdir(f"{setup.sensitive["PATH"]}\\src")
    
    newFilesDir = ""

    print(os.listdir())
    for dir in os.listdir():
        if not("py" in dir or "." in dir):
            print(dir)
            newFilesDir = dir
            os.chdir(f"{dir}")
            for newfile in os.listdir():
                print(newfile)
                if(not "py" in newfile):
                    os.remove(newfile)
                else:
                    shutil.copy(f"{setup.sensitive["PATH"]}\\src\\{dir}\\{newfile}", f"{setup.sensitive["PATH"]}\\src\\{newfile}")

    
    os.chdir("..")
    os.chdir("..")

    os.remove("release.zip")

def downloadUpdate(frm,root):

    setup.sensitive["PATH"] = os.getcwd()
    
    getZip()
    updateFromZip()
    makeEXE()

    setup.sensitive["RELEASE"] = json["name"] 
    setup.saveSens()
    frm.destroy()

    ui.restartNotification(root)

if __name__ == "__main__":
    makeEXE()