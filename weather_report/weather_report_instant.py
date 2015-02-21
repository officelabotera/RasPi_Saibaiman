#!/usr/bin/python
import sys
import sqlite3
import Adafruit_DHT
from datetime import datetime as dt
import subprocess


CURRENT_DIR="/home/tera/Tera/work/weather_report/"


class WeatherReport(object):
  def __init__(self):
    self.id=None
    self.datetime=None
    self.temperature=None
    self.humidity=None
    self.place=None
  def __str__(self):
    return str(self.id)+"|"+ str(self.datetime)+"|"+ str(self.temperature)+"|"+ str(self.humidity)+"|"+ str(self.place)

def get_weather_report():
  sensor=Adafruit_DHT.DHT11
  pin=4
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  if humidity is None or temperature is None:
    return None

  report = WeatherReport()
  report.datetime=dt.now().strftime("%Y-%m-%d %H:%M:%S")
  report.temperature=temperature
  report.humidity=humidity
  report.place="Soil"
  #report.place="Living"
  return report 

def update(report):
  con = sqlite3.connect(CURRENT_DIR+"./database/data.db")
  sql = "insert into weather_report (datetime, temperature, humidity, place) values (?, ?, ?, ?)"
  con.execute(sql, (report.datetime, report.temperature, report.humidity, report.place))
  con.commit()
  con.close()
  
def make_sound():
  cmd = "aplay " + CURRENT_DIR + "./sound/bleep_01.wav"
  subprocess.call( cmd, shell=True  ) 

if __name__ == '__main__':
  report=get_weather_report()
  if report is None:
    print "no data found!"
    sys.exit(0)
  #update(report)
  print "temp: " + str(report.temperature)
  print "humidity: " + str(report.humidity)

  make_sound()
