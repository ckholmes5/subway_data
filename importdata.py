from PIL import Image, ImageFont, ImageDraw
import urllib.request
import datetime
from time import sleep
import math
from config import *
import traceback
import os
from underground import metadata, SubwayFeed
from datetime import timezone
from threading import Thread
import concurrent.futures

blah_blah = 'AZnp59cTqw206YpJgG5WO2DCbHVkOTNE44V8XtJY'
stop_code = 'A19S' # Found in subway_data/StaticData/stops.txt

times = []
out = ''

def func1():
    os.system('sudo /home/pi/Desktop/git/subway_data/rpi-rgb-led-matrix/examples-api-use/./demo --led-rows=16 --led-cols=32 --led-chain=2 -t 10 --led-brightness=20 --led-slowdown-gpio=4 -D 1 -m 0 /home/pi/Desktop/git/subway_data/dynamicimages/dynamictime.ppm')

def func2(ROUTE):
    print('here we are!')
    global feed
    feed = SubwayFeed.get(ROUTE, api_key=blah_blah)

counter = 0

while True:
    try:

        STOP_IDS = {'B': 'BS', 'C': 'CS'}
        for train_line in ['B','C']:
            print('hereeeeeeee', train_line)
            ROUTE = train_line
            if counter == 0:
                feed = SubwayFeed.get(ROUTE, api_key=blah_blah)
            feed = feed.dict()
            current_time = datetime.datetime.now()

            proceed = False
            route = UNIQUE_STOPS[STOP_IDS[ROUTE]]
            print('route: ', route, 'stop: ', UNIQUE_STOPS[STOP_IDS[ROUTE]])

            for entity in feed['entity']:
                if entity['trip_update'] and entity['trip_update']['stop_time_update'] is not None:
                    stops = [update['stop_id'] for update in entity['trip_update']['stop_time_update']]
                    if (route and 'A19S' in stops) | (not route):
                        for update in entity['trip_update']['stop_time_update']:
                            if update['stop_id'] == 'A19S':
                                time = update['arrival']['time']
                                current_time = datetime.datetime.now(timezone.utc)
                                time = math.trunc(((time - current_time).total_seconds()) / 60)
                                times.append(time)

                    else:
                        continue

            times.sort()
            for time in times:
                if time < 0:
                    times.remove(time)
            for time in times[:NUM_TRAINS]:
                out+=str(time)
                out+=str(', ')
            out = out[:-2]
            if len(out) == 0:
                out = 'N/A'
            print(out)
            print('/home/pi/Desktop/git/subway_data/staticimages/' + STOP_IDS[ROUTE] + '.ppm')
            staticimg = Image.open('/home/pi/Desktop/git/subway_data/staticimages/' + STOP_IDS[ROUTE] + '.ppm')

            draw = ImageDraw.Draw(staticimg)
            font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 12)
            draw.text((25, 2), out,(100,100,100), font = font)
            staticimg.save('/home/pi/Desktop/git/subway_data/dynamicimages/dynamictime.ppm')
            times = []
            out = ''

            Thread(target = func1).start()
            Thread(target = func2, args = (ROUTE)).start()
            sleep(2)
            counter += 1

    except Exception:
        print (traceback.format_exc())
