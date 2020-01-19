from tinydb import TinyDB
import requests 
import json
import datetime
import time
import re

ns_db = TinyDB('NS.json')

# the main loop that executes for ever with a sleep of 10 mins
while True:
    response = requests.get('https://www.nspower.ca/library/CurrentLoad/CurrentLoad.json')
    all_curr_loads = json.loads(response.content)
    
    curr_load = float(all_curr_loads[-1]['Base Load'])
    time_stamp_text = all_curr_loads[-1]['datetime']
    time_stamp = float(re.search(r'Date\((.*?)\)', time_stamp_text).group(1))/1000 # time_stamp in YYYY-MM-DD HH:MM:SS
    
    date_time = datetime.datetime.fromtimestamp(time_stamp)
    date_time_str = date_time.__str__()

    last_record = ns_db.get(doc_id=len(ns_db))
    if not last_record or last_record['time'] != date_time_str:
        ns_db.insert({'time': date_time_str, 'Demand': curr_load, 'Supply': 2453.00})
        
    time.sleep(600)
    
    
