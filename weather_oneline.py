import board
import busio
import digitalio
import adafruit_bme280
import datetime

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

temp_c = bme280.temperature
temp_f = temp_c * 9 / 5 + 32
response = "%s,%0.1f,%0.1f,%0.1f" % (datetime.datetime.now(), temp_f, bme280.humidity, bme280.pressure)
print(response)
