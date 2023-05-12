# rasppicoheadphone
pt two with a pi pico 
you will need :
pip install adafruit-blinka
pip install adafruit-circuitpython-ble
pip install pyaudio
pip install pybluez


The first connection is the mic using the PDM microphone connected to pins `GP26` and `GP27` on the board. 

The second connection is to the bluetooth connector using a button connected to pin `GP0` on the board. It is also using Bluetooth to connect to other devices, so it doesn't require any specific pin connections for that purpose.

(OPTIOPNAL) Connect the anc module through I2C or SPI protocols and require specific pins for SDA (data line) and SCL (clock line) communication.
