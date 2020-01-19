import requests
from bs4 import BeautifulSoup
import re

import numpy as np
import datetime, time
from tinydb import TinyDB, Query

def FindDigit(strings):
    """
    Function:
        Find the int digit from a string.
    """
    res = ''.join(filter(lambda i: i.isdigit(), strings))
    val = int(res)
    return val

def FindDigitToFloat(strings):
    """
    Function:
        Find the int digit from a string.
    """
    string_parts = strings.split('.')
    res1 = ''.join(filter(lambda i: i.isdigit(), string_parts[0]))
    res2 = ''.join(filter(lambda i: i.isdigit(), string_parts[1]))
    val = float(res1) + float(res2) / 100.
    return val

def GetDateString(num, length):
    """
    Function:
        Convert date num to string
    """
    return (length - len(str(num))) * '0' + str(num)
    
def GetTimeStamp(time_string):
    """
    Function:
        Get time stamp from the string
    """
    all_digits = FindDigit(time_string)
    output = str(all_digits)[:12]
    return output

def TransferToDate(time_string):
    """
    Function:
        Transfer time stamp to datetime format.
    """
    year = int(time_string[:4])
    month = int(time_string[4:6])
    day = int(time_string[6:8])
    hour = int(time_string[8:10])
    sec = int(time_string[10:12])
    date_time = datetime.datetime(year, month, day, hour, sec)
    return date_time

def OntarioFetch(url):
    """
    Function:
        Download files from website.

    Args:
        Link of the website
    """
    # define a string for finding the month
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    last_time_stamp = soup.findAll("CreatedAt")
    start_time_stamp = soup.findAll("StartDate")
    last_time = GetTimeStamp(str(last_time_stamp[0]))
    start_time = GetTimeStamp(str(start_time_stamp[0]))
    last_time = TransferToDate(last_time)
    start_time = TransferToDate(start_time)
    all_data = soup.findAll("DataSet")
    data =all_data[0].findAll("Data")
    all_val = []
    for i in range(len(data)):
        row = data[i]
        if len(str(row)) >= 35:
            val = FindDigitToFloat(str(row))
        else:
            val = None
        if val is not None:
            all_val.append(val)
    return all_val[-1], last_time, start_time

def OntarioSupplyFetch(supply_url):
    """
    Function:
        Get all the supply data
    """
    response_supply = requests.get(supply_url)
    soup_supply = BeautifulSoup(response_supply.text, "xml")
    last_time_supply = soup_supply.findAll("CreatedAt")
    start_time_supply = soup_supply.findAll("StartDate")
    last_time = GetTimeStamp(str(last_time_supply[0]))
    start_time = GetTimeStamp(str(start_time_supply[0]))
    last_time = TransferToDate(last_time)
    start_time = TransferToDate(start_time)
    all_supply = soup_supply.findAll("DataSet")
    all_supplies = []
    for each_supply in all_supply:
        supply_class = []
        all_rows = each_supply.findAll("Data")
        for each_row in all_rows:
            if len(str(each_row)) >= 30:
                val = FindDigitToFloat(str(each_row))
            else:
                val = None
            if val is not None:
                supply_class.append(val)
        all_supplies.append(np.array(supply_class))
    for i in range(len(all_supplies)):
        if i == 0:
            sum_supply = all_supplies[i]
        else:
            sum_supply += all_supplies[i]
    return sum_supply[-1], last_time, start_time 

def Publishing(freqency):
    """
    Function:
        for keep fetching the lastest data.
    """
    previous_time = 0
    last_time_stamp = str(0)
    db = TinyDB('./ontario.json')
    while True:
        if (time.time() - previous_time) >= freqency:
            ontario_url = "http://ieso.ca/-/media/files/ieso/uploaded/chart/ontario_demand_multiday.xml?la=en"
            ontario_supply_url = "http://ieso.ca/-/media/files/ieso/uploaded/chart/generation_fuel_type_multiday.xml?la=en"
            demand, time_stamp, start_time = OntarioFetch(ontario_url)
            supply, time_stamp_sup, start_time_sup = OntarioSupplyFetch(ontario_supply_url)
            if time_stamp != last_time_stamp:
                print("Ontario, lastest data comes from time:\t" , time_stamp)
                db.insert({'Province': 'Ontario', 'Time': time_stamp.__str__(), 'Demand': demand, 'Supply': supply})
                last_time_stamp = time_stamp
 
if __name__ == "__main__":
   freqency = 60 #sec per time
   Publishing(freqency)
