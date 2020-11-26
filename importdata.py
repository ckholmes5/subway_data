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

blah_blah = 'AZnp59cTqw206YpJgG5WO2DCbHVkOTNE44V8XtJY'
stop = 'A19S'

times = []
out = ''

while True:
    try:
        sleep(1)
        STOP_IDS = {'B': 'BS', 'C': 'CS'}
        for train_line in ['B','C']:
            print('hereeeeeeee', train_line)
            ROUTE = train_line
            feed = SubwayFeed.get(ROUTE, api_key=blah_blah)
            feed = feed.dict()

            current_time = datetime.datetime.now()

            # for stop in STOP_IDS:
            proceed = False
            route = UNIQUE_STOPS[STOP_IDS[ROUTE]]
            print('route: ', route, 'stop: ', UNIQUE_STOPS[STOP_IDS[ROUTE]])

            for entity in feed['entity']:
                if entity['trip_update'] and entity['trip_update']['stop_time_update'] is not None:
                    stops = [update['stop_id'] for update in entity['trip_update']['stop_time_update']]
                    if (route and 'A19S' in stops) | (not route):
                        proceed = True
                        for update in entity['trip_update']['stop_time_update']:
                            if update['stop_id'] == 'A19S':
                                time = update['arrival']['time']
                                current_time = datetime.datetime.now(timezone.utc)
                                time = math.trunc(((time - current_time).total_seconds()) / 60)
                                times.append(time)
                    else:
                        continue

            if proceed:
                print('proeeded!', proceed)
                times.sort()
                for time in times:
                    if time < 0:
                        times.remove(time)
                for time in times[:NUM_TRAINS]:
                    out+=str(time)
                    out+=str(', ')
                out = out[:-2]
                print(out)
                if route:
                    print('/home/pi/Desktop/git/subway_data/staticimages/' + STOP_IDS[ROUTE] + '.ppm')
                    staticimg = Image.open('/home/pi/Desktop/git/subway_data/staticimages/' + STOP_IDS[stop] + '.ppm')
                # else:
                #     print('/home/pi/Desktop/git/subway_data/staticimages/' + stop[0] + stop[3] + '.ppm')
                #     # staticimg = Image.open('/home/pi/Desktop/git/subway_data/staticimages/' + stop[0] + stop[3] + '.ppm')

                draw = ImageDraw.Draw(staticimg)
                font = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf', 60)
                draw.text((25, 4), out,(255,255,255))
                staticimg.save('/home/pi/Desktop/git/subway_data/dynamicimages/dynamictime.ppm')
                times = []
                out = ''

            os.system('sudo /home/pi/Desktop/git/subway_data/rpi-rgb-led-matrix/examples-api-use/./demo --led-rows=16 --led-cols=32 --led-chain=2 -t 5 --led-brightness=20 --led-slowdown-gpio=4 -D 1 -m 0 /home/pi/Desktop/git/subway_data/dynamicimages/dynamictime.ppm')
    except Exception:
        print (traceback.format_exc())




        # Need to classify it as a B or a C stop
        # Know how to classify based on the other stops
