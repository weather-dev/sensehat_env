import time
import datetime
import csv
from sense_hat import SenseHat
import os
import csv
import logging
import json
import math

# Configuration

with open("settings.json", "r") as setting_file:
    setting_data = json.load(setting_file)

logging.basicConfig(filename=setting_data["envtoCSV"]["log_filename"], level=logging.DEBUG)

global theLED
theDelay = setting_data["envtoCSV"]["measurement_delay"]  # The delay between the measurement (in seconds)
theLED = setting_data["envtoCSV"]["LED delay"] # The time of LED lighting during the measurement (in seconds)
if theDelay >= theLED:
    logging.debug("Settings.json settings will be used.")
else:
    theDelay = 300
    theLED = 30
    logging.warning("The settings for measurement delay and LED delay in settings.json are incorrect. Measurement delay used: {}. LED delay used: {}".format(theDelay, theLED))
global delay
delay = theDelay - theLED

cold_water = {"C1": 6.10780, "C2": 17.84362, "C3": 245.425}
water = {"C1": 6.10780, "C2": 17.08085, "C3": 234.175}

fieldname = ["Unix","Date", "Time", "Temp from humidity",
             "Temp from pressure", "Average temp", "Pressure", "Humidity", "Absolute Humidity (g/m3)", "Dew Point"]

f_name = "CSVfile_" + str(datetime.date.today()) + ".csv"

os.chdir(setting_data["envtoCSV"]["output_dir"])  # The directory for saving the CSV files with data

# -------------------- End of Configurations -------------------------------

sense = SenseHat()


def write_headers(names):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writeheader()

    while True:
        env_read(fieldname, delay, theLED)

def dew_point(humidity, temperature, C1, C2, C3):
    relative_hum = humidity / 100
    sat_water_pressure = C1 * math.exp((C2*temperature)/(C3+temperature))
    partial_water_pressure = sat_water_pressure * relative_hum
    top_line = math.log(partial_water_pressure/C1)*C3
    bottom_line = math.log(partial_water_pressure/C1)-C2
    dew_temperature = -top_line/bottom_line
    return dew_temperature

def absolute_humidity(humidity, temperature):
    power_e = (17.67*temperature)/(temperature+243.5)
    e_powered = math.exp(power_e)
    top_line = 6.112 * e_powered * humidity * 2.1674
    bottom_line = 273.15 + temperature
    absolute_hum = top_line/bottom_line
    return absolute_hum

def env_read(names, t, de):
    temph = sense.get_temperature_from_humidity()
    tempp = sense.get_temperature_from_pressure()
    tempa = (temph+tempp)/2
    pres = sense.get_pressure()
    hum = sense.get_humidity()
    dt = time.time()
    d = datetime.date.today()
    ti = time.strftime("%H:%M:%S")
    absolute_hum = absolute_humidity(hum, tempa)
    if tempa < 0:
        dew_temp = dew_point(hum, tempa, **cold_water)
    else:
        dew_temp = dew_point(hum, tempa, **water)
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temp from humidity": temph,
                            "Temp from pressure": tempp, "Average temp": tempa, "Pressure": pres, "Humidity": hum, "Absolute Humidity (g/m3)":absolute_hum, "Dew Point":dew_temp})
    logging.debug("Time: {}. Data written successfully.".format(ti))
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
            env_read(fieldname, delay, theLED)
    else:
        write_headers(fieldname)

try:
    ch(f_name)
except IOError:
    write_headers(fieldname)
