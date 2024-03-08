# 3-Modules System Code

## Disclaimer
This directory contains code for the Raspberry Pi.
I've added a separate directory so we can clone only stuff relative to the Pi.

## Setup Instructions

### 1. Configure Raspberry Pi

#### i) Enable I2C on Raspberry Pi
Open Raspberry Pi configuration tool and enter:
```
sudo raspi-config
```
Navigate to **Interfacing Options** and enable I2C. 
<br/><br/>

#### ii) Configure Audio Output
Navigate to **System Options** > **Audio** and select the desired output (e.g., "3.5mm jack" or "Headphones").
<br/><br/>

#### iii) Enable SPI
Navigate to **Interfacing Options** and enable SPI.
<br/><br/>

#### iv) Enable Wifi
Navigate to **System Options** and enter SSID and password.
<br/><br/>

#### v) Save Changes
Use right/left arrow keys to toggle between **Select** and **Finish** options, DO NOT hit 'esc' on keyboard
<br/><br/>

### 2. Install Software Packages / Libraries
#### i) Install **i2c-tools** package
Install **i2c-tools** package for accelerometer use:
```
sudo apt-get install -y i2c-tools
```
<br/>

#### ii) Install **spidev** library
If pip for Python3 is not installed, use the following command first:
```
sudo apt-get update
sudo apt-get install python3-pip
```

Install the **spidev** Python library for microphone use:
```
sudo pip3 install spidev
```
<br/>


### 3. Test Individual Components
#### i) Detect the Accelerometers:
Use the **i2cdetect** command to check if each accelerometer is detected on the I2C bus.
```
sudo i2cdetect -y [bus number for Pi model, should be 1]
```
Should see the I2C addresses of each accelerometer in the output.
<br/><br/>

#### ii) Check Speaker 
To test the speaker, play a test sound:
```
speaker-test -t sine -f 440 -c 2
```
Determine if the frequencies or channels need to be adjusted. 
<br/><br/>

### 4. Upload Updated Data-Collect Python File to Raspbery Pi
#### i) SSH file
Instructions TBD


## Demonstration Steps

### 1. Play Audio File
The audio file can be played using omxplayer:
```
omxplayer -o local path/to/your/audio.mp3
```
Note: if we need to adjust volume or anything, we can write a script but right now, this is prob the easiest.
<br/><br/>


### 2. Run Script to Start Data Collection

```
python3 data_collect.py
```