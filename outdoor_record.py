import time
import datetime
import os
import csv
import logging
import json
import requests


with open("secret.json", "r") as secrets_file:
    secret_data = json.load(secrets_file)

with open("settings.json", "r") as setting_file:
    setting_data = json.load(setting_file)

logging.basicConfig(filename=setting_data["outdoor"]["log_filename"], level=logging.DEBUG)

fieldname = ["Unix","Date", "Time", "Temperature", "Pressure", "Humidity", "Description"]

f_name = "CSVfile_Out_" + str(datetime.date.today()) + ".csv"

api_key= secret_data["Secret"]["OWM_Key"]
url_complete = "http://api.openweathermap.org/data/2.5/weather?appid=" +api_key+"&q=London&units=metric"

os.chdir(setting_data["outdoor"]["output_dir"])

def write_headers(fieldnames):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        time_now = time.strftime("%H:%M:%S")
        logging.debug("Time: {}. Headers written.".format(time_now))

    while True:
        env_read(fieldname, setting_data["outdoor"]["measurement_delay"])

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

def file_check(theFile):
    with open(theFile,"r") as f:
        theReader = csv.reader(f)
        theNames = next(theReader)
    if theNames == fieldname:
        while True:
            env_read(fieldname, setting_data["outdoor"]["measurement_delay"])
    else:
        write_headers(fieldname)

try:
    file_check(f_name)
except IOError:
    write_headers(fieldname)