import feedparser
from datetime import datetime
import pathlib

URL = 'http://127.0.0.1:1200/xiaoyuzhou/podcast/5e285523418a84a04627767d?limit=50'
IMG_URL = 'https://bts-image.xyzcdn.net/aHR0cHM6Ly9mZGZzLnhtY2RuLmNvbS9ncm91cDg0L00wNy82Mi80Ni93S2c1SGw3LUJBQ1FCNHVrQUFPa1ppVXpjbUkxMDQucG5n.png'


feed = feedparser.parse(URL)
entries = feed['entries']

print(f'loading podcast from {URL}')

size = index = len(entries)

for entry in entries:
    title = entry['title']
    date = entry['published']
    date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
    date = date.strftime('%Y-%m-%d')

    detail = entry['title_detail']
    player = '{% aplayer ' + f'"{title}"' + ' moyu-time ' + ' ' + entry['links'][1]['href']  + ' ' + IMG_URL + ' %}'

    md_builder = \
    f'''---
title: "{title}"
date: {date}
---

{player}

**[Link]({entry['id']})**

## Summary
{entry['summary']}
    '''

    pathlib.Path(f'source/_posts/vol{index}.md').write_text(md_builder)
    print(f'generate md file for source/_posts/vol{index}.md')
    index -= 1