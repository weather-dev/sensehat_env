import time
import datetime
import os
import csv
import logging
import json
import requests

logging.basicConfig(filename="testing.log", level=logging.DEBUG)

fieldname = ["Unix","Date", "Time", "Temperature", "Pressure", "Humidity", "Description"]

delay = 300

f_name = "CSVfile_Out_" + str(datetime.date.today()) + ".csv"

api_key= "855113852123abb0b21fe60d51014cea"
url_complete = "http://api.openweathermap.org/data/2.5/weather?appid=" +api_key+"&q=London&units=metric"

os.chdir(r"E:\Gits\csvFiles")      #"/share/csvFiles"

def write_headers(fieldnames):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        time_now = time.strftime("%H:%M:%S")
        logging.debug("Time: {}. Headers written.".format(time_now))

    while True:
        env_read(fieldname, delay)

def env_read(names, time_delay):
    dt = time.time()
    d = datetime.date.today()
    ti = time.strftime("%H:%M:%S")
    owm_response = requests.get(url_complete).json()
    owm_data = owm_response["main"]
    temperature = owm_data["temp"]
    pressure = owm_data["pressure"]
    humidity = owm_data["humidity"]
    description = owm_response["weather"][0]["description"]
    logging.debug("Temp: {}. Pressure: {}. Humidity: {}. Description: {}".format(temperature, humidity,pressure,description))
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temperature":temperature, "Humidity": humidity, "Pressure":pressure, "Description":description})
    logging.debug("Time: {}. Data written successfully.".format(ti))
    time.sleep(time_delay)

def ch(theFile):
    with open(theFile,"r") as f:
        theReader = csv.reader(f)
        theNames = next(theReader)
    if theNames == fieldname:
        while True:
            env_read(fieldname, delay)
    else:
        write_headers(fieldname)

try:
    ch(f_name)
except IOError:
    write_headers(fieldname)