import setup as setup

from selenium import webdriver
from selenium.webdriver.common.by import By

def findImgs(driver) -> list[str]:
    imgs = driver.find_elements(By.TAG_NAME, "img")
    return imgs

def findMetaTags(driver) -> list[str]: 
    return driver.find_elements(By.TAG_NAME, "meta")

def ifHasAlt(img) -> bool:
    properties = img.get_attribute("alt")

    if(properties == "" or properties == None):
        return False
    return True

def if404(driver) ->bool:
    return False

def ifMetaName(driver) ->bool:
    return False

def ifMetaDesc(driver) ->bool:
    return False

def ifConnects(driver) ->bool:
    return False

if __name__ == "__main__":
    setup.readSens()
    driver = setup.setup()

    print(setup.findAllPages(driver))
    setup.close(driver)