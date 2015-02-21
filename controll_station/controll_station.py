#!/usr/bin/python
import yaml
import time
import sys,os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../soil_monitor')
from monitorsoil import SoilMonitor
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../ssr_switcher')
from ssr_switcher import SSR_Switcher

DB_DIR=os.path.dirname(os.path.abspath(__file__)) + '/database/data.db'

f=open('./conf/conf.yaml', 'r')
CONF=yaml.load(f)
if __name__ == '__main__':
  print "start controll " : datetime.datetime.now()
  print "checking soil tempperature..."
  print "checking soil moisture..."
  soil_monitor = SoilMonitor()
  avg_moisture = soil_monitor.get_average_moisture()
  if avg_moisture < CONF.WATERING_THRESHOLD:
    ssr_switcher=SSR_Switcher()
    print "watering..."
    ssr_switcher.turn_on()
    time.sleep(CONF.WATERING_SEC)
    print "watering stopped"
    ssr_switcher.turn_off()
    con = sqlite3.connect(DB_DIR)
    action='watering'
    log_value='{"watering_sec":'+watering_sec+', "avg_moisture":' + avg_moisture + '}'
    sql = "INSERT INTO control_log (datetime('now', 'localtime'), action, log_value) values (?, ?, ?)"
    con.execute(sql, ( action, log_value))
    con.commit()
    con.close()
