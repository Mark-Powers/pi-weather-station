import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

import board
import busio
import digitalio
import adafruit_bme280

class WeatherHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        if self.path == "/":
            response = b'<img src="/plot.png">'
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
        elif self.path == "/plot.png":
            self.create_fig()
            with open("/home/pi/plot.png", "rb") as f:
                data = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)

    def create_fig(self):
        with open("/home/pi/log.csv") as f:
            date = []
            temp = []
            humid = []
            press = []
            for line in f.readlines():
                parts = line.split(",")
                date.append(datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S.%f"))
                temp.append(float(parts[1]))
                humid.append(float(parts[2]))
                press.append(float(parts[3]))

        ax1 = plt.subplot(311)
        ax1.plot_date(date, temp, 'r-')
        ax1.xaxis.set_major_locator(mpl.dates.DayLocator())
        ax1.xaxis.set_minor_locator(mpl.dates.HourLocator(range(0, 25, 6)))
        ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y-%m-%d"))
        ax1.fmt_xdata = mpl.dates.DateFormatter("%Y-%m-%d")
        ax1.set_ylabel("temperature")

        ax2 = plt.subplot(312)
        ax2.plot_date(date, humid, 'b-')
        ax2.xaxis.set_major_locator(mpl.dates.DayLocator())
        ax2.xaxis.set_minor_locator(mpl.dates.HourLocator(range(0, 25, 6)))
        ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y-%m-%d"))
        ax2.fmt_xdata = mpl.dates.DateFormatter("%Y-%m-%d")
        ax2.set_ylabel("humidity")

        ax3 = plt.subplot(313)
        ax3.plot_date(date, press, 'g-')
        ax3.xaxis.set_major_locator(mpl.dates.DayLocator())
        ax3.xaxis.set_minor_locator(mpl.dates.HourLocator(range(0, 25, 6)))
        ax3.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y-%m-%d"))
        ax3.fmt_xdata = mpl.dates.DateFormatter("%Y-%m-%d")
        ax3.set_ylabel("pressure")
        #fig.autofmt_xdate()

        plt.setp(ax2, xticklabels=[])
        plt.setp(ax3, xticklabels=[])

        fig = plt.gcf()
        fig.set_size_inches(12,8)

        plt.savefig("/home/pi/plot.png")


if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    print("Starting http server")
    http = HTTPServer(("", 80), WeatherHTTPRequestHandler)
    print("serving forever")
    http.serve_forever()



