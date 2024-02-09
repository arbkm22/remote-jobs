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

    job_map = {}
    jobs_list = []
    for ele in jobs_element:
        if ele == 'CURRENT POSITIONS':
            continue
        elif ele == 'Name your dream job':
            break
        else:
            jobs_list.append(ele)
    
    job_map = createOpenplayMap(jobs_list)
    print(f'job_map: {job_map}')

def createOpenplayMap(jobs_list):
    i = 1;
    jobs_map = {}
    for job in jobs_list:
        if (i % 2 == 1):
            jobs_map[job] = jobs_list[i]
        i += 1
    
    for key in jobs_map:
        val = list(jobs_map[key].split(","))
        jobs_map[key] = val;

    return jobs_map

if __name__ == "__main__":
    openplay()