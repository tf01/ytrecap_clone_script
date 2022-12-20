import json
from dateutil import parser
import time


print('Welcome to Tommy\'s youtube history analysing script (TM)!')

# read in json
filename = 'watch-history.json'
print('Opening file: ', filename)
history_file = open(filename, encoding='utf-8')

print('Parsing JSON...')
parsed = json.loads(history_file.read())

# analyse based on num of occurences per channel and video
print('Counting videos from 2022...')
start_count = time.time()
videos = dict()
channels = dict()

total_vid_count = 0

for item in parsed:
    parsed_time = parser.parse(item['time'])

    if parsed_time.year != 2022:
        continue
    
    if 'subtitles' not in item:
        continue

    total_vid_count += 1
    
    if item['subtitles'][0]['name'] in channels:
        channels[item['subtitles'][0]['name']] += 1
    else:
        channels[item['subtitles'][0]['name']] = 1

    if item['title'] in videos:
        videos[item['title']] += 1
    else:
        videos[item['title']] = 1

end_count = time.time()
taken = round(end_count - start_count, 2)
print(f'Count completed! Time taken: {taken}')

# sort
sorted_videos = dict(sorted(videos.items(), key=lambda item: item[1], reverse=True))
sorted_channels = dict(sorted(channels.items(), key=lambda item: item[1], reverse=True))

# print occurences
top_num = 500

print('Here are the results!')
print('Num of (total) videos watched: ', total_vid_count)
print('Num of (distinct) videos watched: ', len(sorted_videos))
print('Num of (distinct) channels watched: ', len(sorted_channels))

print(top_num, 'most watched videos:')
count = 0
for (key, value) in sorted_videos.items():
    count += 1
    title = str(key).replace('Watched ', '')
    print(f'#{str(count).zfill(3)}: {value} watches of {title}')
    if(count >= top_num):
        break

print(top_num, 'most watched channels:')
count = 0
for (key, value) in sorted_channels.items():
    count += 1
    print(f'#{str(count).zfill(3)}: {value} from {key}')
    if(count >= top_num):
        break