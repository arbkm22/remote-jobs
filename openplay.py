import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By

OPENPLAY_URL = 'https://openplay.co/careers/'

def openplay():
    driver = webdriver.Chrome()
    driver.get(OPENPLAY_URL)
    time.sleep(3)
    curr_pos = driver.find_elements(By.CLASS_NAME, "section")
    jobs_element = []
    for job in curr_pos:
        if ('CURRENT POSITIONS' in job.text):
            jobs_element = job.text.split('\n')

    # TODO: create map of the jobs
    job_map = {}
    jobs_list = []
    for ele in jobs_element:
        if ele == 'CURRENT POSITIONS':
            continue
        elif ele == 'Name your dream job':
            break
        else:
            jobs_list.append(ele)
    
    print(f'jobs: {jobs_list}')


if __name__ == "__main__":
    openplay()
    