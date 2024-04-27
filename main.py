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
    'anime-1':    'https://abema.tv/timetable/channels/abema-anime',
    'anime-2':    'https://abema.tv/timetable/channels/abema-anime-2',
    'isekai-1':   'https://abema.tv/timetable/channels/isekai-anime',
    'isekai-2':   'https://abema.tv/timetable/channels/isekai-anime-2',
    'lovecomedy': 'https://abema.tv/timetable/channels/lovecomedy-anime',
    'dailylife':  'https://abema.tv/timetable/channels/dailylife-anime',
    'late-night': 'https://abema.tv/timetable/channels/late-night-anime',
    'anime-live': 'https://abema.tv/timetable/channels/anime-live',
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

print(json.dumps(json_data, indent=2, ensure_ascii=False))
driver.quit()
