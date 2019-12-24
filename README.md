# Sense Hat Weather Recorder

The project uses python to record environmental data from a raspberry pi SenseHat and outdoor data for a given city.
The data collected by a raspberry pi can then be sent to an email or uploaded to server/dropbox.

## Hardware

This section goes through the hardware used for the running of this project.

### Required

The hardware required for running the project:

1. Raspberry Pi 2 or higher
2. SenseHat
3. Power Adapter

### Optional

The hardware that is recomended for the running of this project:

1. Ethernet Cable
2. GPIO Ribbon Cable (40 pin)
3. GPIO Male to Male Coupler

## Installation and Set Up

- [ ] Installation
  - [ ] Get a copy of the code
  - [ ] Install python modules
- [ ] Setting up
  - [ ] Get API keys
  - [ ] Settings files
- [ ] Running the code

### Installation

#### Getting a copy

To get a copy of the code, run `git clone https://github.com/weather-dev/sensehat_env.git` on the pi. This will copy the content of this GitHub repo into `./sensehat_env` directory. If you would like to save the content in a different folder, run `git clone https://github.com/weather-dev/sensehat_env.git {folder}`. THis will save the repo content into `./folder` directory.

- [ ] Installation
  - [x] Get a copy of the code
  - [ ] Install python modules
- [ ] Setting up
- [ ] Running the code

#### Installing modules

Install the python modules required for the running of the project by using `pip install -r requirements.txt`. It is recommended that this is done in a virtual environment as to prevent affecting any of your currently installed modules. For more information on using the python virtual environments on raspberry pi see [GeekTechStuff about Virtual Environments](https://geektechstuff.com/2019/01/14/creating-a-virtual-python-environment-python/)

- [x] Installation
  - [x] Get a copy of the code
  - [x] Install python modules
- [ ] Setting up
- [ ] Running the code

### Setting Up

#### Getting API Keys

To use the program you need to obtain an API key from [OpenWeatherMap (OWM)](https://home.openweathermap.org/). To do this, register a free account with the OWM and go to the ___API keys___ section of the website. Then create an API key and store it somewhere safe. It will be used in the next section of the set up.

To use the dropbox upload functionality, you need to create an app on DropBox using [DropBox Developers](https://www.dropbox.com/developers/apps/create) (see screenshot below for app creation)

![DropBox Developers Page](screenshots\DropBox_Developers.png)

Once the app is created, generate an access token in the OAuth 2 section of the page. Keep this token safe as it will be used in the later section of the setting up.

- [x] Installation
- [ ] Setting up
  - [x] Get API keys
  - [ ] Email and SCP set up
  - [ ] Settings files
- [ ] Running the code

#### Email and SCP set up

To use the emailing functionality, it is recommended to use a separate new gmail email address as it will need to allow for "less secure apps" to run. To set up the access for less secure apps, go to the [Less secure apps](https://myaccount.google.com/lesssecureapps) section of the google website and turn on the "Allow less secure apps"

![Less Secure Apps](screenshots\Gmail_setup.png)

For an explanation of setting up the SCP upload to a server, follow the instructions on the ["How to use the SCP without password](https://alvinalexander.com/linux-unix/how-use-scp-without-password-backups-copy)

- [x] Installation
- [ ] Setting up
  - [x] Get API keys
  - [x] Email and SCP set up
  - [ ] Settings files
- [ ] Running the code

### Settings Files

The project uses two settings files to keep all of the basic settings in the same place. These files are:

- [`secret.json`](secret.json)
- [`settings.json`](settings.json)

#### Secret.json

The `secret.json` file is used to store secret information. It is therefore important that you **DO NOT** share the content of this file with anyone.

The file has the following layout:

```json
{
    "Secret": {
        "OWM_Key": "",
        "DBX_tokken":""
    },
    "Emails":{
        "from_address":"",
        "to_address":"",
        "from_address_pasw":""
    },
    "Calculations":{
        "Temperature_High":"",
        "Temperature_Low":""
    },
    "scp_send":{
        "server_loc":""
    }
}
```

- `OWM_Key` is used to store the API key obtained from the OpenWeatherMap at the start of the [section](###Getting-API-Keys).
- `DBX_tokken` is used to store the Dropbox access token obtained at the start of the [section](###Getting-API-Keys).
- `from_address`stores the email adress used to send an email containing the data collected by the SenseHat to the address stored in `to address`
- `from_address_pasw` stores the password for the `from address`
- `Temperature_High` stores the webhooks URL to activate the IFTTT action when temperature is too high
- `Temperature_Low` stores the webhooks URL to activate the IFTTT action when temperature is too low
- `server_loc` stores the ip address for a server to send the data to via SCP.

#### settings.json

The `settings.json` file is used to store the settings used by the programs. This file is set up to have default values out of the box. However, feel free to experiment with these.

The file has the following layout:

```json
{
    "envtoCSV": {
        "log_filename": "./logs/envtoCSV_tests.log",
        "comment_1": "Measurement delay must be larger than LED delay",
        "measurement_delay": 10,
        "LED delay": 5,
        "output_dir": "./csvFiles"
    },
    "outdoor": {
        "log_filename": "./logs/outdoor_tests.log",
        "measurement_delay": 5,
        "output_dir": "./csvFiles"
    },
    "Uploader":{
        "log_filename":"./logs/uploader.log"
    },
    "Emails":{
        "log_filename":"./logs/emails.log"
    },
    "Averages":{
        "log_filename":"./logs/averages.log",
        "Number_of_measurements":20,
        "Low_temperature_limit":15,
        "High_temperature_limit":25
    },
    "scp_send":{
        "log_filename":"./logs/scp_upload.log"
    }
}
```

- `envtoCSV` controls the behaviour of the `envtoCSV.py`
  - `log_filename` sets the location and file name of the log
  - `measurement_delay` set the delay in seconds between the measurements taken by the SenseHat
  - `LED delay` sets the length of the status LED light in seconds.
    - Note: `measurement_delay` must be longer than the `LED delay`
  - `output_dir` sets the output relative directory for the csv data files to be stored in

- `outdoor` controls the behaviour of the `outdoor_record.py`
  - `log_filename` sets the location and file name of the log
  - `measurement_delay` set the delay in seconds between the requests being made to the OWM API
  - `output_dir` sets the output relative directory for the csv data files to be stored in

- `Uploader` controls the behaviour of the `scp_uploader.py`
  - `log_filename` sets the location and file name of the log

- `Emails` controls the behaviour of the `send_email.py`
  - `log_filename` sets the location and file name of the log

- `Averages` controls the behaviour of the `calculate_average.py`
  - `log_filename` sets the location and file name of the log
  - `Number_of_measurements` sets the number of measurements used to calculate the average temperature
  - `Low_temperature_limit` sets the temperature at which the `Temperature_Low` webhook in [`secret.json`](####secret.json) is activated
  - `High_temperature_limit` sets the temperature at which the `Temperature_High` webhook in [`secret.json`](####secret.json) is activated

- `scp_send` controls the behaviour of the `scp_uploader.py`
  - `log_filename` sets the location and file name of the log

- [x] Installation
- [x] Setting up
  - [x] Get API keys
  - [x] Email and SCP set up
  - [x] Settings files
- [ ] Running the code

### Running the code

#### Checking the code

To check that the code is set up appropriately run the following commands:

1. `python3 envtoCSV.py` for 5 minutes
2. `python3 outdoor_record.py` for 5 minutes
3. `python3 uploader.py`
4. `python3 calculate_average.py`

#### Automatic running

To set up the data collection and upload scripts to run autonomously you can use crontab on the RaspberryPi.

1. Make the included shell scripts executable by running `chmod 755 envtoCSV_launcher.sh` and `chmod 755 emailing_launcher.sh`
2. Add a crontab log directory by running `mkdir logs`
3. Open crontab editor with `sudo crontab -e`
4. Enter:

  ``` shell
  0 0 * * * sudo reboot
  0 1 * * * sh /directory_for_sensehat/sensehat_env/emailing_launcher.sh > /home/pi/logs/emailing_cronlog 2>&1
  @reboot sh /directory_for_sensehat/sensehat_env/envtoCSV_launcher.sh > /home/pi/logs/envtoCSV_cronlog 2>&1
  ```

5. Test the set up by running `sudo reboot`. A status LED on the SenseHat matrix should light up to indicate that the scripts are running properly.

- [x] Installation
- [x] Setting up
  - [x] Get API keys
  - [x] Email and SCP set up
  - [x] Settings files
- [x] Running the code
