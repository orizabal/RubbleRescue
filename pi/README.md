# 3-Modules System Code

## Disclaimer
This directory contains code for the Raspberry Pi.
I've added a separate directory so we can clone only stuff relative to the Pi.

## Setup Instructions

### 1. Enable I2C on Raspberry Pi:
Open Raspberry Pi configuration tool and enter:
```
sudo raspi-config
```

Navigate to **interfacing options** and enable I2C. Reboot Raspberry Pi.
<br/>

### 2. Install Software
Install **i2c-tools** package:
```
sudo apt-get install -y i2c-tools
```

### 3. Detect the Accelerometers:
Use the **i2cdetect** command to check if each accelerometer is detected on the I2C bus.
```
sudo i2cdetect -y [bus number for Pi model]
```

Should see the I2C addresses of each accelerometer in the output.

### 4. Run Script

```
python3 modules_test.py
```