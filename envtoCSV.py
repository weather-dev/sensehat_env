import time
import datetime
import csv
from sense_hat import SenseHat
import os
import csv
import requests
import json

# Configuration

global theLED
theDelay = 300  # The delay between the measurement (in seconds)
theLED = 30  # The time of LED lighting during the measurement (in seconds)

global delay
delay = theDelay - theLED

# setting the url for the open weather map (OWM)
api_key = "855113852123abb0b21fe60d51014cea"
city_name_main = 'London'
complete_url_current_main = "http://api.openweathermap.org/data/2.5/weather?appid=" + \
    api_key+"&q="+city_name_main+"&units=metric"

fieldname = ["Unix","Date", "Time", "Temp from humidity",
             "Temp from pressure", "Average temp", "Pressure", "Humidity", "Outside Temp"]

f_name = "CSVfile_" + str(datetime.date.today()) + ".csv"

os.chdir("/share/csvFiles")  # The directory for saving the CSV files with data

# -------------------- End of Configurations -------------------------------

sense = SenseHat()


def write_headers(names):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writeheader()

    while True:
        env_read(fieldname, delay, theLED, complete_url_current_main)


def env_read(names, t, de, url):
    response = requests.get(url)
    x = response.json()
    y = x["main"]
    current_temp = y["temp"]
    temph = sense.get_temperature_from_humidity()
    tempp = sense.get_temperature_from_pressure()
    tempa = (temph+tempp)/2
    pres = sense.get_pressure()
    hum = sense.get_humidity()
    dt = time.time()
    d = datetime.date.today()
    ti = time.strftime("%H:%M:%S")
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temp from humidity": temph,
                            "Temp from pressure": tempp, "Average temp": tempa, "Pressure": pres, "Humidity": hum, "Outside Temp": current_temp})
    sense.set_pixel(3, 3, 255, 100, 100)
    time.sleep(de)
    sense.clear()
    time.sleep(t)

def ch(theFile):
    with open(theFile,"r") as f:
        theReader = csv.reader(f)
        theNames = next(theReader)
    if theNames == fieldname:
        while True:
            env_read(fieldname, delay, theLED, complete_url_current_main)
    else:
        write_headers(fieldname)

try:
    ch(f_name)
except IOError:
    write_headers(fieldname)
