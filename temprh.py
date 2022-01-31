"""
'temp_humidity.py'
==================================
Example of sending analog sensor
values to an Adafruit IO feed.

Author(s): Brent Rubell

Tutorial: learn.adafruit.com/adafruit-io-basics-temperature-and-humidity

Dependencies:
    - Adafruit IO Python Client
        (https://github.com/adafruit/io-client-python)
    - Adafruit_Python_DHT
        (https://github.com/adafruit/Adafruit_Python_DHT)
"""

# import standard python modules.
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# import Adafruit Blinka
import board
from digitalio import DigitalInOut, Direction, Pull
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
# import adafruit dht library.
import Adafruit_DHT

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# Raspberry Pi pin configuration:
RST = 24     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 5

# Pin connected to DHT22 data pin
DHT_DATA_PIN = 26

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '197e3e4992d8ccaf9bc2902b53dae60d1df0a986'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = 'onespeedonly'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
temperature_feed = aio.feeds('tempup')
humidity_feed = aio.feeds('humidityup')

# Set up DHT22 Sensor.
dht22_sensor = Adafruit_DHT.DHT22

# switch set up
switch = digitalio.DigitalInOut(board.D12)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
disp.begin()

time.sleep(1)

disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()


while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht22_sensor, DHT_DATA_PIN)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        # Send humidity and temperature feeds to Adafruit IO
        temperature = '%.2f'%(temperature)
        humidity = '%.2f'%(humidity)
        aio.send(temperature_feed.key, str(temperature))
        aio.send(humidity_feed.key, str(humidity))
    else:
        print('Failed to get DHT22 Reading, trying again in ', DHT_READ_TIMEOUT, 'seconds')
    if switch.value == False
        # false means switch has been closed and connected to ground
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 24), "Temperature and Humidity of Down Downstairs", font=font, fill=255)
        draw.text((0, 28), "Temperature = " + temperature + " deg F", font=font, fill=255)
        draw.text((0, 32), "Humidity = " + humidity + " %", font=font, fill=255)
        disp.image(image)
        disp.display()
    else:
        disp.clear()
        disp.display()
    # Timeout to avoid flooding Adafruit IO
    time.sleep(DHT_READ_TIMEOUT)
    