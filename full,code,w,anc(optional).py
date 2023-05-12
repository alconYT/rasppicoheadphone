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

# Initialize the microphone and ANC module
mic = audiobusio.PDMIn(board.GP26, board.GP27, sample_rate=16000, bit_depth=16)
anc = ANCModule()

# Define the Bluetooth device names for each device
DEVICE1_NAME = "Device1"
DEVICE2_NAME = "Device2"

# Set up the device connection state variables
device1_connected = False
device2_connected = False

# Main loop
while True:
    # Check for Bluetooth connections
    if ble.connected:
        # Get the name of the connected device
        device_name = ble.connections[0].name

        # Set the device connection state based on the device name
        if device_name == DEVICE1_NAME:
            device1_connected = True
            device2_connected = False
        elif device_name == DEVICE2_NAME:
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

    # Apply ANC processing to the audio data
    processed_samples = anc.process(raw_samples)

    # Compute the root mean square (RMS) of the audio data
    samples = list(processed_samples)
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
