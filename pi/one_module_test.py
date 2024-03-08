import smbus
import time
import spidev
import subprocess

bus = smbus.SMBus(1)
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)

# ACCELEROMETER
# Specify unique I2C addresses for each accelerometer
accelerometer1_address = 0x1C # ADDR Pin Configuration: GND

def read_word(address, reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    value = (high << 8) + low
    return value

try:
    while True:
        # Read data from the accelerometer
        accel1_x = read_word(accelerometer1_address, 0x01)  # Replace with the appropriate register addresses
        accel1_y = read_word(accelerometer1_address, 0x03)
        accel1_z = read_word(accelerometer1_address, 0x05)

        print(f"Accelerometer 1 - X: {accel1_x}, Y: {accel1_y}, Z: {accel1_z}")

        # If all accelerometer values are less than 20, break the loop
        if accel1_x < 20 and accel1_y < 20 and accel1_z < 20:
            break

        time.sleep(1)

except KeyboardInterrupt:
    pass


# MICROPHONE RECORDING
def record_audio():
    filename = "recorded_audio.wav"  # You can save as WAV format
    duration = 10  # Record for 10 seconds
    subprocess.run(["arecord", "-d", str(duration), "-f", "cd", "-c", "1", filename])  # Record using arecord

try:
    # Record audio for 10 seconds
    record_audio()
    print("Audio recording completed.")
except Exception as e:
    print("Error occurred while recording audio:", e)
finally:
    spi.close()


