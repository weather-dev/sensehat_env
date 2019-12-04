import time
import datetime
import os
import csv
import logging
import json
import requests
import math

with open("secrets.json", "r") as secrets_file:
    secret_data = json.load(secrets_file)

logging.basicConfig(filename=secret_data["log_filename"], level=logging.DEBUG)

fieldname = ["Unix","Date", "Time", "Temperature", "Pressure", "Humidity", "Abs Humidity", "Description"]

f_name = "CSVfile_Out_" + str(datetime.date.today()) + ".csv"

api_key= secret_data["OWM_Key"]
url_complete = "http://api.openweathermap.org/data/2.5/weather?appid=" +api_key+"&q=London&units=metric"

os.chdir(secret_data["output_dir"])

def write_headers(fieldnames):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        time_now = time.strftime("%H:%M:%S")
        logging.debug("Time: {}. Headers written.".format(time_now))

    while True:
        env_read(fieldname, secret_data["measurement_delay"])

def absolute_humidity(humidity, temperature):
    power_e = (17.67*temperature)/(temperature+243.5)
    e_powered = math.exp(power_e)
    top_line = 6.112 * e_powered * humidity * 2.1674
    bottom_line = 273.15 + temperature
    absolute_hum = top_line/bottom_line
    return absolute_hum


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
    absolute_hum = absolute_humidity(humidity, temperature)
    logging.debug("Temp: {}. Pressure: {}. Humidity: {}. Description: {}, Absolute humidity: {}".format(temperature, humidity,pressure,description, absolute_hum))
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temperature":temperature, "Humidity": humidity, "Pressure":pressure, "Description":description, "Abs Humidity":absolute_hum})
    logging.debug("Time: {}. Data written successfully.".format(ti))
    time.sleep(time_delay)

def file_check(theFile):
    with open(theFile,"r") as f:
        theReader = csv.reader(f)
        theNames = next(theReader)
    if theNames == fieldname:
        while True:
            env_read(fieldname, secret_data["measurement_delay"])
    else:
        write_headers(fieldname)

try:
    file_check(f_name)
except IOError:
    write_headers(fieldname)