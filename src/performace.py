import logging
import requests
import json


logger = logging.getLogger(__name__)


def openPage(URL:str):
    request = requests.get(URL)
    return request.json()

def generateURL(webpage:str):
    return f"https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url={webpage}&category=PERFORMANCE&key={apikey}"

def runPerformance(baseURL:str):
    r = openPage(generateURL(baseURL))

if __name__ == "__main__":
    print(json.dumps(openPage(generateURL("https://www.tda.com/")), indent=2))