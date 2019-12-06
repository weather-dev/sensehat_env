import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime as dt
import json
import logging

with open("settings.json", "r") as setting_file:
    setting_data = json.load(setting_file)
with open("secrets_noupload.json", "r") as secret_file:
    secret_data = json.load(secret_file)

logging.basicConfig(filename=setting_data["Emails"]["log_filename"], level=logging.DEBUG)

# --------------------Configuration--------------------------------------
fromaddr = secret_data["Emails"]["from_address"]
toaddr = secret_data["Emails"]["to_address"]
passwd = secret_data["Emails"]["from_address_pasw"]
file_date =str( dt.date.today() - dt.timedelta(days = 1) )
emailSubject = "CSV File " + file_date
emailText = "CSV file from " + file_date
filename = "/CSVfile_"+file_date+".csv"
# ----------------End of Configuration-----------------------------------

filePath = setting_data["envtoCSV"]["output_dir"] + filename

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = emailSubject

body = emailText

msg.attach(MIMEText(body, 'plain'))

attachment = open(filePath, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, passwd)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

logging.debug("Email sent successfully.")