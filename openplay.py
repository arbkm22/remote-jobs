import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By

OPENPLAY_URL = 'https://openplay.co/careers/'

def openplay():
    driver = webdriver.Chrome()
    driver.get(OPENPLAY_URL)
    page_source = driver.page_source
    print(f'page source: ${page_source}')

if __name__ == "__main__":
    openplay()
    