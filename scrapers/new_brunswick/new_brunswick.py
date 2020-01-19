from tinydb import TinyDB, Query
import requests 
import time
from bs4 import BeautifulSoup as bs
import csv


nb_db = TinyDB('NB.json')

while True:
    response = requests.get('https://tso.nbpower.com/Public/en/op/market/report_list.aspx?path=\load%20forecast\hourly')
    
    html_soup = bs(response.text, 'html.parser')
    ref_row = html_soup.find('a', id='lv_2')
    ref = ref_row['href']

    last_hour_csv_ref_text = html_soup.find('a', id='lv_2')
    last_hour_csv_ref = last_hour_csv_ref_text['href']

    last_hour_csv = requests.get(last_hour_csv_ref, allow_redirects=True)

    open('./NB_latest_hour.csv', 'wb').write(last_hour_csv.content)
    with open('./NB_latest_hour.csv', 'r') as f:
        reader = csv.reader(f)
        data_list = list(reader)

    current_data = data_list[0] # current load related data in the first row
    time_text = current_data[0] # current time stamp
    time_stamp_str = "{}-{}-{} {}:{}:{}".format(time_text[0:4], time_text[4:6], time_text[6:8], int(time_text[8:10])-1, time_text[10:12], time_text[12:14])
    
    demand = float(current_data[1]) # current load
                            
    last_record = nb_db.get(doc_id=len(nb_db))
    if not last_record or last_record['time'] != time_stamp_str:
        nb_db.insert({'Time': time_stamp_str, 'Demand': demand, 'Supply': 00.00})
        
    time.sleep(20)
    break;

