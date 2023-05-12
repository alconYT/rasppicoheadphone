import board
import digitalio
import busio
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

# Define the Bluetooth device names for each device
DEVICE1_NAME = "Device1"
DEVICE2_NAME = "Device2"

# Set up the device connection state variables
device1_connected = False
device2_connected = False

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

    # Wait a bit before checking again
    time.sleep(0.1)

