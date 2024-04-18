#!/usr/bin/env python

import json
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

urls = {
    'anime1': 'https://abema.tv/timetable/channels/abema-anime',
    'anime2': 'https://abema.tv/timetable/channels/abema-anime-2',
    'anime3': 'https://abema.tv/timetable/channels/abema-anime-3',
    'live1':  'https://abema.tv/timetable/channels/anime-live',
    'live2':  'https://abema.tv/timetable/channels/anime-live2',
    'live3':  'https://abema.tv/timetable/channels/anime-live3'
}

json_data = [{}, {}, {}]

for day in range(0, 3):
    date = datetime.date.today() + datetime.timedelta(days=day)
    json_data[day]['date'] = date.strftime('%m/%d')
    json_data[day]['timetable'] = {}

for channel, url in urls.items():
    driver.get(url)
    sleep(3)
    timetablecolumns = driver.find_elements(By.CLASS_NAME, "com-timetable-TimetableColumn")

    for day in range(0, 3):
        items = timetablecolumns[day].find_elements(By.CLASS_NAME, "com-timetable-TimetableItem")
        y0 = items[0].rect['y']
        json_data[day]['timetable'][channel] = []

        for i in items:
            title = i.find_element(By.CLASS_NAME, "com-a-CollapsedText__container").text.replace('\n', '')[2:]
            height = i.rect['height']
            y = i.rect['y'] - y0
            json_data[day]['timetable'][channel].append({'title': title, 'height': height, 'y': y})

print(json.dumps(json_data, indent=2))
driver.quit()
