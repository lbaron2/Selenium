import requests
import setup

def update():
    setup.readSens()
    makeReqURL()
    global json
    json = requests.get(url).json()
    if(needUpdate):
        downloadUpdate()

def makeReqURL():
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

def downloadUpdate():
    zip_url = json['zipball_url']
    r = requests.get(zip_url, allow_redirects=True)
    with open('release.zip', 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    print(update())