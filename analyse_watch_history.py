import json
import time

outlines = []
def print_output(input_string):
    print(input_string)
    outlines.append(input_string + '\n')
    
print_output('Welcome to Tommy\'s youtube history analysing script (TM)!')

# read in json
filename = 'watch-history.json'
print_output(f'Opening file: {filename}')
history_file = open(filename, encoding='utf-8')

print_output('Parsing JSON...')
parsed = json.loads(history_file.read())

history_file.close()

# analyse based on num of occurences per channel and video
print_output('Counting videos from 2022...')
start_count = time.time()
videos = dict()
channels = dict()

total_vid_count = 0

for item in parsed:

    if str(item['time'])[0:4] != '2022':
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
print_output(f'Count completed! Time taken: {taken}')

# sort
sorted_videos = dict(sorted(videos.items(), key=lambda item: item[1], reverse=True))
sorted_channels = dict(sorted(channels.items(), key=lambda item: item[1], reverse=True))

# print occurences
top_num = 500

print_output('Here are the results!')
print_output(f'Num of (total) videos watched: {total_vid_count}')
print_output(f'Num of (distinct) videos watched: {len(sorted_videos)}')
print_output(f'Num of (distinct) channels watched: {len(sorted_channels)}')

print_output(f'{top_num} most watched videos:')
count = 0
for (key, value) in sorted_videos.items():
    count += 1
    title = str(key).replace('Watched ', '')
    print_output(f'#{str(count).zfill(3)}: {value} watches of {title}')
    if(count >= top_num):
        break

print_output(f'{top_num} most watched channels:')
count = 0
for (key, value) in sorted_channels.items():
    count += 1
    print_output(f'#{str(count).zfill(3)}: {value} from {key}')
    if(count >= top_num):
        break

# write out to file
print('Writing to file...')
outfile = open('output.txt', 'w', encoding="utf-8")
outfile.writelines(outlines)
outfile.close()