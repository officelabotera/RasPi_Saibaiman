#/usr/bin/python
import sys
import sqlite3
from webiopi.devices.analog.mcp3x0x import MCP3204
from datetime import datetime as dt

CURRENT_DIR="/home/pi/Tera/work/soil_monitor/"
DB_DIR=os.path.dirname(os.path.abspath(__file__)) + '/database/data.db'

class SoilMonitor(object):
  def __init__(self):
    self.id=None
    self.datetime=None
    self.moisture=None
    self.raw_value=None

  def __str__(self):
   return str(self.id)+"|"+str(self.datetime)+"|"+str(self.moisture)
 
  def get_average_moisture(self, past_hours=24):
   date_from=datetime.datetime.now().timedelta(hours=-past_hours)
   con = sqlite3.connect(DB_DIR)
   sql = 'SELECT avr(moisture) FROM soil_monitor WHERE datetime > "%s";' % (date_from)
   avl_moisture=con.execute(sql).get()
   return avl_moisture

def get_soil_moisture():
  mcp0 = MCP3204()
  raw_value =  mcp0.analogReadAll().get(0)
  rate = raw_value/3200.0
  moisture=rate * 950.0

  monitor=SoilMonitor()
  monitor.datetime=dt.now().strftime("%Y-%m-%d %H:%M:%S")
  monitor.raw_value=raw_value
  monitor.moisture=moisture
  return monitor

def update(monitor):
  con = sqlite3.connect(DB_DIR)
  sql = "insert into soil_monitor (datetime, moisture, raw_value) values (?, ?, ?)"
  con.execute(sql, (monitor.datetime, monitor.moisture, monitor.raw_value))
  con.commit()
  con.close()
    

if __name__ == '__main__':
  monitor=get_soil_moisture()
  if monitor is None:
    print "no data found!"
    sys.exit(0)
  update(monitor)
  print monitor

