from selenium import webdriver
from selenium.webdriver.common.by import By
def readSens() -> None:
    """Reads in values that are not supposed to be on github through a file called "sensitive.txt", such as website access passwords or API keys"""
    import os
    global sensitive

    sensitive = {}
    if "sensitive.txt" in os.listdir():
        with open(r"sensitive.txt", "r") as txt:
            for line in txt:
                words = line.strip().split("::")
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

if __name__ == "__main__":
    readSens()
    login(setup())