#!/usr/bin/env python

import json
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

config = [
    {
        'channel_selector_info': {
            'display_name': 'アニメ',
            'anchor_x_min': 0.1,
            'anchor_x_max': 0.3,
            'font_size': 6
        },
        'channels': [
            {
                'display_name': 'アニメ１',
                'anchor_x_min': 0.0,
                'anchor_x_max': 0.5,
                'url': 'https://abema.tv/timetable/channels/abema-anime'
            }, {
                'display_name': 'アニメ２',
                'anchor_x_min': 0.5,
                'anchor_x_max': 1.0,
                'url': 'https://abema.tv/timetable/channels/abema-anime-2'
            }
        ]
    }, {
        'channel_selector_info': {
            'display_name': '異世界\nファンタジー',
            'anchor_x_min': 0.3,
            'anchor_x_max': 0.5,
            'font_size': 3
        },
        'channels': [
            {
                'display_name': '異世界・ファンタジー１',
                'anchor_x_min': 0.0,
                'anchor_x_max': 0.5,
                'url': 'https://abema.tv/timetable/channels/isekai-anime'
            }, {
                'display_name': '異世界・ファンタジー２',
                'anchor_x_min': 0.5,
                'anchor_x_max': 1.0,
                'url': 'https://abema.tv/timetable/channels/isekai-anime-2'
            }
        ]
    }, {
        'channel_selector_info': {
            'display_name': 'ラブコメ\n日常青春',
            'anchor_x_min': 0.5,
            'anchor_x_max': 0.7,
            'font_size': 3
        },
        'channels': [
            {
                'display_name': 'ラブコメ',
                'anchor_x_min': 0.0,
                'anchor_x_max': 0.5,
                'url': 'https://abema.tv/timetable/channels/lovecomedy-anime'
            }, {
                'display_name': '日常青春',
                'anchor_x_min': 0.5,
                'anchor_x_max': 1.0,
                'url': 'https://abema.tv/timetable/channels/dailylife-anime'
            }
        ]
    }, {
        'channel_selector_info': {
            'display_name': '深夜\nアニライ',
            'anchor_x_min': 0.7,
            'anchor_x_max': 0.9,
            'font_size': 3
        },
        'channels': [
            {
                'display_name': '深夜アニメ',
                'anchor_x_min': 0.0,
                'anchor_x_max': 0.5,
                'url': 'https://abema.tv/timetable/channels/late-night-anime'
            }, {
                'display_name': 'アニライ',
                'anchor_x_min': 0.5,
                'anchor_x_max': 1.0,
                'url': 'https://abema.tv/timetable/channels/anime-live'
            }
        ]
    }
]

days = [
    {
        'display_name': '',
        'anchor_x_min': 0.125,
        'anchor_x_max': 0.375,
        'font_size': 6
    }, {
        'display_name': '',
        'anchor_x_min': 0.375,
        'anchor_x_max': 0.625,
        'font_size': 6
    }, {
        'display_name': '',
        'anchor_x_min': 0.625,
        'anchor_x_max': 0.875,
        'font_size': 6
    }
]

json_data = {
    'date_selector': [],
    'timetable_header': [],
    'timetable': [],
    'channel_selector': []
}

nicovrc_proxy = 'https://nicovrc.net/proxy/?'

for day in range(len(days)):
    date = datetime.date.today() + datetime.timedelta(days=day)
    json_data['date_selector'].append(days[day])
    json_data['date_selector'][-1]['display_name'] = date.strftime('%m/%d')

for channel_group in config:
    json_data['channel_selector'].append(channel_group['channel_selector_info'])
    channel_group_data = []
    channel_group_header_data = []
    
    for channel in channel_group['channels']:
        url = channel['url']
        channel_group_header_data.append(channel)
        channel_group_header_data[-1]['url'] = nicovrc_proxy + url
        channel_data = []

        driver.get(url)
        sleep(3)
        timetablecolumns = driver.find_elements(By.CLASS_NAME, "com-timetable-TimetableColumn")

        for day in range(len(days)):
            channel_data_in_a_day = []
            items = timetablecolumns[day].find_elements(By.CLASS_NAME, "com-timetable-TimetableItem")
            y0 = items[0].rect['y']

            for i in items:
                title = i.find_element(By.CLASS_NAME, "com-a-CollapsedText__container").text.replace('\n', '')[2:]
                height = i.rect['height']
                y = i.rect['y'] - y0
                channel_data_in_a_day.append({'title': title, 'height': height, 'y': y})
                
            channel_data.append(channel_data_in_a_day)
        channel_group_data.append(channel_data)
    json_data['timetable'].append(channel_group_data)
    json_data['timetable_header'].append(channel_group_header_data)

print(json.dumps(json_data, indent=2, ensure_ascii=False))
driver.quit()
