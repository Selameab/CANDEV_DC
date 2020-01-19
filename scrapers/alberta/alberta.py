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

def GetDateString(num, length):
    """
    Function:
        Convert date num to string
    """
    return (length - len(str(num))) * '0' + str(num)
    
def AlbertaFetch(url):
    """
    Function:
        Download files from website.

    Args:
        Link of the website
    """
    # define a string for finding the month
    months_string = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                    "Sep", "Oct", "Nov", "Dec"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.findAll("table")

    for table_i in table:
        rows = table_i.findAll("tr")
        for row_i in rows:
            content = row_i.find(text = re.compile("Alberta Total Net Generation"))
            time_content = row_i.find(text = re.compile("Last Update"))
            if content is not None:
                target_row = row_i
                subrows = target_row.findAll("tr")
                if len(subrows) > 1:
                    for subrow_i in subrows:
                        generation = subrow_i.find(text = re.compile("Alberta Total Net Generation"))
                        internal_load = subrow_i.find(text = re.compile("Alberta Internal Load "))
                        if generation is not None:
                            str_content = str(subrow_i)
                            generation_val = FindDigit(str_content)
                        if internal_load is not None:
                            str_content = str(subrow_i)
                            internal_load_val = FindDigit(str_content)
            if time_content is not None:
                time_target_row = row_i
                time_subrows = time_target_row.findAll("tr")
                time_info = None
                if len(time_subrows) == 1 and time_info is None:
                    time_info = str(time_subrows[0]).split(' ')
                    month = months_string.index(time_info[3]) + 1
                    day = FindDigit(time_info[4])
                    year = FindDigit(time_info[5])
                    actual_time_parts = time_info[6].split(':')
                    hour = FindDigit(actual_time_parts[0])
                    sec = FindDigit(actual_time_parts[1])
                    time_stamp = GetDateString(year, 4) + GetDateString(month, 2) + \
                                GetDateString(day, 2) + GetDateString(hour, 2) + \
                                GetDateString(sec, 2)
    return generation_val, internal_load_val, time_stamp

def Publishing(freqency):
    """
    Function:
        for keep fetching the lastest data.
    
    Args:
        generation_val          ->          Alberta Total Net Generation
        internal_load_val       ->          Alberta Internal Load (AIL)
        time_stamp              ->          time stamp for the lastest data
        frequency               ->          freshing frequency of fetching the data
    """
    previous_time = 0
    last_time_stamp = str(0)
    db = TinyDB('./alberta.json')
    while True:
        if (time.time() - previous_time) >= freqency:
            previous_time = time.time()
            alberta_link = "http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"
            alberta_total_net_generation, alberta_internal_load, time_stamp = AlbertaFetch(alberta_link)
            if time_stamp != last_time_stamp:
                print("lastest data comes from time:" + time_stamp)
                db.insert({'Province': 'Alberta', 'Time': time_stamp, 'Demand': alberta_internal_load, 'Supply': alberta_total_net_generation})
                last_time_stamp = time_stamp

if __name__ == "__main__":
    freq = 30 # sec per time
    Publishing(freq)
