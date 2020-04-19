from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
#import nyct_subway_pb2
import urllib.request
import datetime
from time import sleep
import math
import os
from config import *
import traceback

times = []
out = ''

while True:
	try:
		sleep(20)
		mtafeed = gtfs_realtime_pb2.FeedMessage()
		response = urllib.request.urlopen('http://datamine.mta.info/mta_esi.php?key=' + MTA_KEY + '&feed_id=26')
		mtafeed.ParseFromString(response.read())
		current_time = datetime.datetime.now()
		for stop in STOP_IDS:
			proceed = False
			route = UNIQUE_STOPS[STOP_IDS[stop]]
			for entity in mtafeed.entity:
				if entity.trip_update:
					stops = [update.stop_id for update in entity.trip_update.stop_time_update]
					if (route and route in stops) | (not route):
						proceed = True
						for update in entity.trip_update.stop_time_update:
							if update.stop_id == stop:
								time = update.arrival.time
								if time <= 0:
									time = update.departure.time
								time = datetime.datetime.fromtimestamp(time)
								time = math.trunc(((time - current_time).total_seconds()) / 60)
								times.append(time)
					else:
						continue

			if proceed:
				times.sort()
				for time in times:
					if time < 0:
						times.remove(time)
				for time in times[:NUM_TRAINS]:
					out+=str(time)
					out+=str(', ')
				out = out[:-2]
				if route:
					staticimg = Image.open('staticimages/' + STOP_IDS[stop] + '.ppm')
				else:
					staticimg = Image.open('staticimages/' + stop[0] + stop[3] + '.ppm')

				draw = ImageDraw.Draw(staticimg)
				#font = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf', 12)
				font = ImageFont.truetype('/Library/Fonts/Helvetica-Regular.ttf', 14)
				draw.text((22, 3), out,(200,200,200),font=font)
				staticimg.save('dynamicimages/dynamictime.ppm')
				times = []
				out = ''
			# os.system('./rpi-rgb-led-matrix/led-matrix -r 16 -c 2 -t 5 -b 50 -D 1 -m 5000 dynamicimages/dynamictime.ppm')
	except Exception:
		print (traceback.format_exc())




# Need to classify it as a B or a C stop
# Know how to classify based on the other stops
#
