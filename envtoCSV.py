import time
import datetime
import csv
from sense_hat import SenseHat
import os
import csv
import logging
import json

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

fieldname = ["Unix","Date", "Time", "Temp from humidity",
             "Temp from pressure", "Average temp", "Pressure", "Humidity"]

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


def env_read(names, t, de):
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
                            "Temp from pressure": tempp, "Average temp": tempa, "Pressure": pres, "Humidity": hum})
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
