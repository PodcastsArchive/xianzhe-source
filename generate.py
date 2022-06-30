from html import entities
import feedparser
from datetime import datetime
import pathlib
import urllib.request
import os
import re

URL = 'http://127.0.0.1:1200/xiaoyuzhou/podcast/5e285523418a84a04627767d?limit=50'
ONLINE_PREFIX = 'https://podcastsarchive.github.io/xianzhetime'
LOCAL_HOST_PREFIX = 'http://localhost:4000/xianzhetime'
PREFIX = ONLINE_PREFIX
IMG_URL = 'https://podcastsarchive.github.io/xianzhetime/image/img.jpg'
AUTHOR = ' KillTime '
AUDIO_DIR = './source/audio/'

feed = feedparser.parse(URL)
audio_len = len(os.listdir(AUDIO_DIR))
all_entries = feed['entries']
entries_len = len(all_entries)
entries = all_entries
# entries = all_entries[:entries_len - audio_len]

print(f'new entries {len(entries)}')
print(f'loading podcast from {URL}')

size = index = entries_len

# for entry in entries:
#     link = entry['links'][1]['href']
#     urllib.request.urlretrieve(link, f"./source/audio/vol{index}.m4a")
#     index -= 1

index = size

for entry in entries:
    title = entry['title'].replace('"', '')
    date = entry['published']
    date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    # audio = entry['links'][1]['href']
    audio = f'{PREFIX}/audio/vol{index}.m4a'
    detail = entry['title_detail']
    player = '{% aplayer ' + f'"{title}"' + AUTHOR + ' ' + audio + ' ' + IMG_URL + ' %}'
    summary = entry['summary']
    summary = re.sub('style=\".*?\"', '', summary)
    durnation = entry['itunes_duration']
    length = entry['links'][1]['length']
    md_builder = \
    f'''---
title: "{title}"
date: {date}
duration: '{ durnation }'
media: { audio }
image: { IMG_URL }
length: { length }
type: 'audio/mpeg'
---

{player}

**[Link]({entry['id']})**

## Summary
{summary}
    '''

    pathlib.Path(f'source/_posts/vol{index}.md').write_text(md_builder)
    print(f'generate md file for source/_posts/vol{index}.md')
    index -= 1