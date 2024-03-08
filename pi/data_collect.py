import smbus
import time
import RPi.GPIO as GPIO
from gpiozero import MCP3008
import wavio
import sounddevice as sd
import numpy as np

bus = smbus.SMBus(1)
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)

## ACCELEROMETER

# GPIO Pin Configuration for MUX
S1_PIN = 17      # GPIO pin for MUX S1
S0_PIN = 27      # GPIO pin for MUX S0

# Accelerometer Addresses
accel_1_address = 0x1D  # Address of accel #1
accel_shared_address = 0x1C  # Shared address of accels #2 and #3

# Function to set MUX channel
def set_mux_channel(channel):
    GPIO.output(S1_PIN, channel & 0x02)
    GPIO.output(S0_PIN, channel & 0x01)

# Function to read accelerometer data
def read_accel_data(accel_addr):
    # Read accelerometer data
    data = bus.read_i2c_block_data(accel_addr, 0x00, 6)
    
    # Convert data to acceleration values
    x = (data[0] << 8 | data[1]) >> 4
    y = (data[2] << 8 | data[3]) >> 4
    z = (data[4] << 8 | data[5]) >> 4
    
    return x, y, z

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(S1_PIN, GPIO.OUT)
GPIO.setup(S0_PIN, GPIO.OUT)

try:
    while True:
        # Read data from accelerometer 1
        x1, y1, z1 = read_accel_data(accel_1_address)
        print("Accelerometer 1: X={}, Y={}, Z={}".format(x1, y1, z1))
        
        # Switch to MUX channel 0 (Accelerometer #2)
        set_mux_channel(0)
        time.sleep(0.1)  # Delay to stabilize readings
        
        # Read data from accelerometer 2
        x2, y2, z2 = read_accel_data(accel_shared_address)
        print("Accelerometer 2: X={}, Y={}, Z={}".format(x2, y2, z2))
        
        # Switch to MUX channel 1 (Accelerometer #3)
        set_mux_channel(1)
        time.sleep(0.1)  # Delay to stabilize readings
        
        # Read data from accelerometer 3
        x3, y3, z3 = read_accel_data(accel_shared_address)
        print("Accelerometer 3: X={}, Y={}, Z={}".format(x3, y3, z3))
        
        time.sleep(2)  # Delay for 2 seconds before next reading

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    GPIO.cleanup()  # Clean up GPIO pins

## MICROPHONE
    
# Initialize MCP3008 ADC for microphone readings 
MIC_1_CS = 8 # Module #1
MIC_2_CS = 19 # Module #2
MIC_3_CS = 20 # Module #3

# Initialize MCP3008 ADC objects for each microphone
mic1_adc = MCP3008(channel=0)
mic2_adc = MCP3008(channel=1)
mic3_adc = MCP3008(channel=2)

# Function to record audio from microphone for 10 seconds
def record_audio(mic_num, duration=10, sample_rate=44100):
    print(f"Recording from Microphone {mic_num} for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait for recording to complete
    print(f"Recording from Microphone {mic_num} complete.")
    return recording, sample_rate

try:
    for mic_num, mic_adc in enumerate([mic1_adc, mic2_adc, mic3_adc], start=1):
        # Record audio for 10 seconds
        recording, sample_rate = record_audio(mic_num)

        # Save recording as .wav file
        filename = f"mic_{mic_num}.wav"
        print(f"Saving recording from Microphone {mic_num} as {filename}...")
        wavio.write(filename, recording, sample_rate, sampwidth=2)
        print(f"Recording from Microphone {mic_num} saved as {filename}")

except KeyboardInterrupt:
    print("Recording interrupted by user.")
