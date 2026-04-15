from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
from pathlib import Path
import logging



logger = logging.getLogger(__name__)
def readSens() -> None:
    """Reads in values that are not supposed to be on github through a file called "config", such as website access passwords or API keys"""
    global sensitive

    logger.info("Reading Sensitive")
    sensitive = {}    
    os.chdir(f"{os.getcwd()}\\json")
    if "config.json" in os.listdir():
        with open(r"config.json", "r") as file:
            sensitive = json.load(file)
    os.chdir("..")
    
def setup() -> object:
    """Makes the browser for the selenium interactions"""

    driver = webdriver.Chrome()
    driver.get(sensitive["LINK"])
    logger.info("Setting up webdriver")
    
    return driver


def login(driver) -> object:
    """Sets up future tests by logging into the website"""

    passwordBox = driver.find_element(by=By.NAME, value="password")
    passwordBox.send_keys(sensitive["PASSWORD"])
    passwordBox.send_keys("\n")

    return driver

def close(driver) -> None:
    driver.close()

def findLinks(driver) -> list[str]:
    imgs = driver.find_elements(by=By.TAG_NAME, value ="a")
    return imgs

def findAllLinksOnOnePage(page,driver):
    difLinks = []
    sensitive["LINK"] = page

    driver.get(page)
    page = findLinks(driver)

    for link in page:
        link = link.get_attribute("href")
        if (link not in difLinks) and ("#" not in link):
            difLinks.append(link)

    return difLinks       

def findAllPages(driver):
    links = findLinks(driver)

    seenLinks = []
    pageLinks = []
    unSeenLinks = []

    originalLink = sensitive["LINK"]
    seenLinks.append(sensitive["LINK"])

    for page in links:
            page = page.get_attribute("href")
            if not(page in unSeenLinks) and not(page in seenLinks):
                unSeenLinks.append(page)    
        
    for link in unSeenLinks:
        if link[len(link)-1:] == "/": #prevents testing same link, just with / at the end
            continue
        elif "#" in link: #prevents testing redirects on pages
            continue
        elif not(originalLink in link): #prevents from going outside of the origin link (etc, not exploring all of linkdin)
            continue

        pageLinks = findAllLinksOnOnePage(link,driver)

        for page in pageLinks:
            if not(page in unSeenLinks) and not(page in seenLinks):
                unSeenLinks.append(page)   


        seenLinks.append(link) 
        
    sensitive["LINK"] = originalLink

    return seenLinks

def errorCountDifferent(errorCount, priorErrorCount):
    if(errorCount != priorErrorCount):
            return True
    return False

def ifError(test, page, newPage, type, output) -> int:
    if(not test):
        print(f"{type}",end="<br>",file=output)
        return 1
    return 0

def setLink(newLink:str):
    """Updates Link from UI"""
    sensitive["LINK"] = newLink
    saveSens()

def saveSens():
    logger.info("Saving Sensitive JSON")
    if "json" in os.listdir():
        with open(r"json//config.json", "w+") as txt:
            json.dump(sensitive,txt, ensure_ascii=False, indent=4)
    else:
        logger.info("Cannot find JSON FOLDER")

if __name__ == "__main__":
    readSens()
    sensitive["LINK"] = ""
    saveSens()
