import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

HASHNODE_URL = 'https://hashnode.crew.work/jobs'

def createHashnodeMap(raw_jobs_list, jobs_dict):
    prev_job = None
    for raw_jobs in raw_jobs_list:
        if raw_jobs in jobs_dict:
            prev_job = raw_jobs
        else:
            jobs_dict[prev_job].append(raw_jobs)

    return jobs_dict

def hashnode():
    driver = webdriver.Chrome()
    driver.get(HASHNODE_URL)
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="html.parser")
    jobs_li = driver.find_elements(By.CLASS_NAME, "jobs-list")
    jobs_list_names = driver.find_elements(By.CLASS_NAME, "job-item__name")
    jobs_name = []
    for item in jobs_list_names:
        jobs_name.append(item.text)
    raw_jobs_list = []
    jobs_string = ""
    for item in jobs_li:
        jobs_string = item.text

    raw_jobs_list = jobs_string.split('\n')
    # print(raw_jobs_list)

    jobs_dict = {}
    perks = []

    for string in raw_jobs_list:
        if string in jobs_name:
            if string in jobs_dict.keys():
                print(string)
            else:
                jobs_dict[string] = []
        else: 
            perks.append(string)
    
    # print(f'jobs_dict: {jobs_dict}')
    # print(f'perks: {perks}')
    jobs_dict = createHashnodeMap(raw_jobs_list, jobs_dict)

    return jobs_dict