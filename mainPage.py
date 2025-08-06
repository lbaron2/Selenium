from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(keep_alive=True)

driver = driver.get("https://tda.com/")