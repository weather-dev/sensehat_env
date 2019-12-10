import pandas as pd
import logging
import requests
import json
import datetime
import os

with open("secret.json", "r") as secrets_file:
    secret_data = json.load(secrets_file)
with open("settings.json", "r") as settings_file:
    settings_data = json.load(settings_file)

logging.basicConfig(
    filename=settings_data["Averages"]["log_filename"], level=logging.DEBUG)

file_name = "CSVfile_" + str(datetime.date.today()) + ".csv"
os.chdir(settings_data["envtoCSV"]["output_dir"])

def data_handle_pd(measure_num=10, file_name=file_name, min_temp=20, max_temp=27):
    df = pd.read_csv(file_name)
    calc_df = df.tail(int(measure_num))
    temp_average = round(calc_df.loc[:, "Average temp"].mean(), 3)
    logging.debug("Settings: Measurement number: {}, File name analysed: {}, Low temperature limit: {}C, High temperature limit: {}C".format(
        measure_num, file_name, min_temp, max_temp))
    if temp_average < min_temp:
        print("It's cold here!")
        requests.post(secret_data["Calculations"]["Temperature_Low"],
                      params={"value1": temp_average, "value2": "none", "value3": "none"})
        logging.debug("Notification sent")
    elif temp_average > max_temp:
        print("It's too hot here!")
        requests.post(secret_data["Calculations"]["Temperature_High"],
                      params={"value1": temp_average, "value2": "none", "value3": "none"})
        logging.debug("Notification sent")
    else:
        print("The temperature is just right.")
    return temp_average


print("The average temperature is: {}C.".format(data_handle_pd(
    file_name=file_name, measure_num=settings_data["Averages"]["Number_of_measurements"], min_temp=settings_data["Averages"]["Low_temperature_limit"], max_temp=settings_data["Averages"]["High_temperature_limit"])))
