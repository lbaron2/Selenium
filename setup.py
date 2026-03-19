from selenium import webdriver
from selenium.webdriver.common.by import By
import os


def readSens() -> None:
    """Reads in values that are not supposed to be on github through a file called "sensitive.txt", such as website access passwords or API keys"""
    global sensitive
    global keys

    sensitive = {}
    keys = []
    if "sensitive.txt" in os.listdir():
        with open(r"sensitive.txt", "r") as txt:
            for line in txt:
                words = line.strip().split("::")
                keys.append(words[0].upper())
                sensitive[words[0].upper()] = words[1]

def setup() -> object:
    """Makes the browser for the selenium interactions"""

    driver = webdriver.Chrome()
    driver.get(sensitive["LINK"])
    
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

def ifError(test, page, type, output) -> int:
    if(not test):
        print(f"There was a {type} problem with {page}",file=output)
        return 1
    return 0

def setLink(newLink:str):
    """Updates Link from UI"""
    sensitive["LINK"] = newLink
    saveSens()

def saveSens():
    if "sensitive.txt" in os.listdir():
        with open(r"sensitive.txt", "w+") as txt:
            lineCount = len(keys)
            for i in range(0,lineCount):
                print(f"{keys[i]}::{sensitive[keys[i]]}",file=txt)


if __name__ == "__main__":
    readSens()
