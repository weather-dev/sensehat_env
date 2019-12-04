import time
import datetime
import csv
from sense_hat import SenseHat
import os
import csv
import logging
import math
# Configuration

logging.basicConfig(filename="testing.log", level=logging.DEBUG)

global theLED
theDelay = 300  # The delay between the measurement (in seconds)
theLED = 30  # The time of LED lighting during the measurement (in seconds)

global delay
delay = theDelay - theLED

fieldname = ["Unix","Date", "Time", "Temp from humidity",
             "Temp from pressure", "Average temp", "Pressure", "Humidity"]

f_name = "CSVfile_" + str(datetime.date.today()) + ".csv"

os.chdir("/share/csvFiles")  # The directory for saving the CSV files with data

# -------------------- End of Configurations -------------------------------

sense = SenseHat()


def write_headers(names):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writeheader()

    while True:
        env_read(fieldname, delay, theLED)


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
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temp from humidity": temph,
                            "Temp from pressure": tempp, "Average temp": tempa, "Pressure": pres, "Humidity": hum, "Absolute Humidity (g/m3)":absolute_hum})
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
