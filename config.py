#Change this file name to config.py and update appropriately

MTA_KEY = '71c041c935ba89d698abb8cd778a47e6' #obtain one at http://web.mta.info/developers/developer-data-terms.html
NUM_TRAINS = 2  #the number of trains to display for each station/direction combination  
STOP_IDS = {'A19S': 'BS', 'A19N': 'CS'}  #an array of stations/directions that you would like displayed. Find these in the stations file in staticdatax
UNIQUE_STOPS = {'BS': 'D03', 'CS': 'A11N'} # dictionary of stations unique stops