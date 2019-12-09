import pandas as pd
import logging
import requests
import json

logging.basicConfig(filename="averages.log", level=logging.DEBUG)

file_name = r"csvFiles\CSVfile_Gen_2019-12-02.csv"

with open("secrets.json", "r") as secrets_file:
    secret_data = json.load(secrets_file)

def data_handle_pd(measure_num=10, file_name=file_name, min_temp=20, max_temp=27):
    df = pd.read_csv(file_name)
    calc_df = df.tail(int(measure_num))
    temp_average = round(calc_df.loc[:, "Temperature"].mean(), 3)
    logging.debug("Settings: Measurement number: {}, File name analysed: {}, Low temperature limit: {}C, High temperature limit: {}C".format(
        measure_num, file_name, min_temp, max_temp))
    if temp_average < min_temp:
        print("It's cold here!")
        requests.post("https://maker.ifttt.com/trigger/<COMMAND>/with/key/<KEY>",
                      params={"value1": temp_average, "value2": "none", "value3": "none"})
        logging.debug("Notification sent")
    elif temp_average > max_temp:
        print("It's too hot here!")
        requests.post("https://maker.ifttt.com/trigger/<COMMAND>/with/key/<KEY>",
                      params={"value1": temp_average, "value2": "none", "value3": "none"})
        logging.debug("Notification sent")
    else:
        print("The temperature is just right.")
    return temp_average


print("The average temperature is: {}C.".format(data_handle_pd(
    file_name=file_name, measure_num=20, min_temp=15, max_temp=20)))
