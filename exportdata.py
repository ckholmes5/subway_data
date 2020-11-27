import os
while True:
    os.system('sudo /home/pi/Desktop/git/subway_data/rpi-rgb-led-matrix/examples-api-use/./demo --led-rows=16 --led-cols=32 --led-chain=2 -t 10 --led-brightness=20 --led-slowdown-gpio=4 -D 1 -m 0 /home/pi/Desktop/git/subway_data/dynamicimages/C_dynamictime.ppm')
    os.system('sudo /home/pi/Desktop/git/subway_data/rpi-rgb-led-matrix/examples-api-use/./demo --led-rows=16 --led-cols=32 --led-chain=2 -t 10 --led-brightness=20 --led-slowdown-gpio=4 -D 1 -m 0 /home/pi/Desktop/git/subway_data/dynamicimages/B_dynamictime.ppm')
