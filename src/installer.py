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
        zip_ref.extractall("")

    newFileDir = ""
    
    for dir in os.listdir():
        absPath = os.path.join(setup.sensitive["PATH"],dir)
        if("lbaron2" in dir and os.path.isdir(absPath)):
            newFileDir = absPath
            print(f"current dir: {absPath}")
            os.chdir(f"{dir}")
            for innerDir in os.listdir():
                absPathInner = os.path.join(absPath,innerDir)
                print(f"current file/folder: {absPathInner}")
                if(os.path.isdir(absPathInner)):
                    print(f"\t {absPathInner} -> {os.path.join(setup.sensitive["PATH"],innerDir)}")
                    shutil.copytree(src=absPathInner,dst=os.path.join(setup.sensitive["PATH"],innerDir),dirs_exist_ok=True)
                elif(os.path.isfile(absPathInner)):
                    print(f"\t {absPathInner} -> {os.path.join(setup.sensitive["PATH"],innerDir)}")
                    shutil.copyfile(src=absPathInner,dst=os.path.join(setup.sensitive["PATH"],innerDir))
    os.chdir("..")

    shutil.rmtree(newFileDir)
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