#!/usr/bin/python
import sys
import sqlite3
from webiopi.devices.analog.mcp3x0x import MCP3204
from datetime import datetime as dt
import RPi.GPIO as GPIO

DB_DIR=os.path.dirname(os.path.abspath(__file__)) + '/database/data.db'


class SSR_Switcher(object):
  def __init__(self, io_number):
    self.IO_NO = io_number
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.IO_NO, GPIO.OUT)

  def __del__(self):
    print 'GPIO cleanup'
    GPIO.cleanup()

  def turn_on(self):
    GPIO.output(self.IO_NO, True)
    self.update()
    
  def turn_off(self):
    GPIO.output(self.IO_NO, False)
    self.update()

  def get_status(self):
    return GPIO.input(self.IO_NO)


  def update(self):
    con = sqlite3.connect(DB_DIR)
    sql = "insert into switch_log (datetime, io_number, status) values (datetime('now'), ?, ?)"
    con.execute(sql, (self.IO_NO, self.get_status()))
    con.commit()
    con.close()


  def __str__(self):
    return str(self.id)+"|"+str(self.datetime)+"|"+str(self.moisture)

