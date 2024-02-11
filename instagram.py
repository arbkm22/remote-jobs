import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By

IG_URL = 'https://about.instagram.com/about-us/careers'

def instagram():
    driver = webdriver.Chrome()
    driver.get(IG_URL)
    time.sleep(3)
    jobs_list = driver.find_elements(By.ID, "instagram_about_site_careers_filter_results_id")
    jobs_list_div = driver.find_elements(By.CLASS_NAME, "_af-z")
    jobs = ""
    jobs_li = []

    locations = []
    duration = ""
    position = ""
    tags = []

    for item in jobs_list_div:
        jobs += item.text
        jobs_li.append(item.text.split('\n'))

    job_data = {}

    for item in jobs_li:
        temp_li = []
        duration = item[0]
        locations = item[1].split('|')
        pos = item[2].split(',')
        position = pos[0]
        tags = pos[1:]
        temp_li.append(duration)
        temp_li.append(locations)
        temp_li.append(tags)
        job_data[position] = temp_li
        
        # print(f'duration: {duration} | locs: {locations} | pos: {position}')
    # print(f'job_data: {job_data}')
    # job_data = createIgMap(duration, locations, position, tags)
    job_data = createInstagramData(job_data)
    print(f'job_data: {job_data}')

def createIgMap(duration, locations, position, tags):
    igMap = {}
    igMap['duration'] = duration
    igMap['locations'] = locations
    igMap['position'] = position
    igMap['tags'] = tags
    return igMap
    
def createInstagramData(job_data):
    print(f'job_data: {job_data}')
    job_mod = {}
    for key in job_data.keys():
        job_mod[key] = {
            "company": "Instagram",
            "website": IG_URL,
            "duration": job_data[key][0],
            "locations": job_data[key][1],
            "tags": job_data[key][2]
        }
    return job_mod

if __name__ == "__main__":
    instagram()