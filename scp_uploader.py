import os
import datetime as dt
import json
import logging

with open("secret.json", "r") as secret_file:
    secret_data = json.load(secret_file)
with open("settings.json", "r") as setting_file:
    setting_data = json.load(setting_file)

logging.basicConfig(filename=setting_data["scp_send"]["log_filename"], level=logging.DEBUG)
server_location = secret_data["scp_send"]["server_loc"]

file_date = str( dt.date.today() - dt.timedelta(days = 1) )
file_name = "CSVfile_{}.csv".format(file_date)

os.chdir(setting_data["envtoCSV"]["output_dir"])

logging.debug("Working directory after swap: {}".format(os.getcwd()))

command_run = "scp {} {}".format(file_name, server_location)

os.system(command_run)
logging.debug("Command '{}' run successfully".format(command_run))