#!/usr/bin/python
import sys
import time
import RPi.GPIO as GPIO

spi_clk  = 11
spi_mosi = 10
spi_miso = 9
spi_ss   = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(spi_mosi, GPIO.OUT)
GPIO.setup(spi_miso, GPIO.IN)
GPIO.setup(spi_clk,  GPIO.OUT)
GPIO.setup(spi_ss,   GPIO.OUT)

while True:
    time.sleep(2)

    for ch in range(8):
        GPIO.output(spi_ss,   False)
        GPIO.output(spi_clk,  False)
        GPIO.output(spi_mosi, False)
        GPIO.output(spi_clk,  True)
        GPIO.output(spi_clk,  False)

        cmd = (ch | 0x18) << 3
        for i in range(5):
            if (cmd & 0x80):
                GPIO.output(spi_mosi, True)
            else:
                GPIO.output(spi_mosi, False)
            cmd <<= 1
            GPIO.output(spi_clk, True)
            GPIO.output(spi_clk, False)
        GPIO.output(spi_clk, True)
        GPIO.output(spi_clk, False)
        GPIO.output(spi_clk, True)
        GPIO.output(spi_clk, False)

        value = 0
        for i in range(12):
            value <<= 1
            GPIO.output(spi_clk, True)
            if (GPIO.input(spi_miso)):
                value |= 0x1
            GPIO.output(spi_clk, False)

        if ch > 0:
            sys.stdout.write(" ")
        GPIO.output(spi_ss, True)
        sys.stdout.write(str(value))

    sys.stdout.write("\n")
