import dropbox 
import sys
import json
import datetime as dt
import logging

with open("secrets_noupload.json", "r") as secrets_file:
    secret_data = json.load(secrets_file)

with open("settings.json", "r") as setting_file:
    setting_data = json.load(setting_file)

logging.basicConfig(filename=setting_data["Uploader"]["log_filename"], level=logging.DEBUG)

access_token =  secret_data["Secret"]["DBX_tokken"] 
logging.debug("Your access token is: {}".format(access_token))
dbx = dropbox.Dropbox(access_token)

dbx.users_get_current_account()
logging.debug("Account data: {}".format(dbx.users_get_current_account()))

def uploader():
    file_date =str( dt.date.today() - dt.timedelta(days = 1) )
    filename = "CSVfile_"+file_date+".csv"
    upload_file = 'csvFiles/{}'.format(filename)
    upload_destination = '/csvFiles/Bedroom/'+filename
    with open(upload_file, 'rb') as f:
        dbx.files_upload(f.read(), upload_destination)
        logging.debug("File: {} uploaded to Dropbox. Location: {}".format(filename, upload_destination))



uploader()