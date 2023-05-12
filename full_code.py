import board
import digitalio
import busio
import audiobusio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import time
import pyaudio
import wave
import bluetooth

# Set up the Bluetooth connection
ble = adafruit_ble.BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.start_advertising(advertisement)

# Set up the keyboard and button pins
keyboard = Keyboard()
button_pin = digitalio.DigitalInOut(board.GP0)
button_pin.switch_to_input(pull=digitalio.Pull.UP)

# Define the threshold for audio level detection
THRESHOLD = 5000

# Initialize the microphone
mic = audiobusio.PDMIn(board.GP26, board.GP27, sample_rate=16000, bit_depth=16)

# Define the Bluetooth device address of the receiver board
receiver_address = "00:11:22:33:44:55"

# Set up the PyAudio audio output stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

# Open the audio file to play
with wave.open("test.wav", "rb") as wavefile:
    # Create a Bluetooth socket and connect to the receiver board
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((receiver_address, 1))

    # Read and play the audio data in chunks
    chunk_size = 1024
    data = wavefile.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wavefile.readframes(chunk_size)

    # Close the Bluetooth socket and audio output stream
    sock.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Main loop
while True:
    # Check for Bluetooth connections
    if ble.connected:
        # Get the name of the connected device
        device_name = ble.connections[0].name

        # Set the device connection state based on the device name
        if device_name == "Device1":
            device1_connected = True
            device2_connected = False
        elif device_name == "Device2":
            device1_connected = False
            device2_connected = True

    # Check the button state and switch between devices
    if not button_pin.value:
        if device1_connected:
            keyboard.press(Keycode.ALT, Keycode.TAB)
            keyboard.release_all()
        elif device2_connected:
            keyboard.press(Keycode.CONTROL, Keycode.TAB)
            keyboard.release_all()

    # Read audio data from the microphone
    raw_samples = mic.record(512)

    # Compute the root mean square (RMS) of the audio data
    samples = list(raw_samples)
    sum_squares = sum(float(s ** 2) for s in samples)
    rms = int((sum_squares / len(samples)) ** 0.5)

    # Check if the audio level exceeds the threshold
    if rms > THRESHOLD:
        print("Audio level:", rms)
        # Perform an action here, such as triggering an event or sending a notification
        # For demonstration purposes, we simply sleep for 2 seconds
        time.sleep(2)

    # Wait a bit before checking again
    time.sleep(0.1)
