import random
import csv
import scipy.integrate as integrate
import numpy as np

from serial.tools.list_ports import comports
import serial
# from serial import Serial
import serial.tools.list_ports
import time
import math as mt

i ,dis1= 0,0
class Communication:
    portName = 'com3'
    dummyPlug = False
    # ports = serial.tools.list_ports.comports()

    ser = serial.Serial()

    def __init__(self):
        self.baudrate = 115200
        self.port = comports()
        self.portlist = [port for port, desc, hwid in sorted(self.port)]
        if serial.Serial() is not open:
            try:
                self.ser = serial.Serial(self.portName, self.baudrate)
                self.ser.flushInput()
                self.ser.flushOutput()
                # self.ser.write("get")
                # sleep(1) for 100 millisecond delay
                # 100ms dely
                time.sleep(.1)
            except serial.serialutil.SerialException:
                # print("Can't open : ", self.portName)
                self.dummyPlug = True
                print("Dummy mode activated")
        else:
            print("error")

    def close(self):
        if self.ser.isOpen():
            self.ser.close()
        else:
            print(self.portName, " it's already closed")

    def getData(self):
        global i,dis1
        value = self.ser.readline()  # read line (single value) from the serial port
        decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
        # print(len(value))
        value_chain = decoded_bytes.split(",")

        if len(value_chain) == 3:
            x1 = float(value_chain[0])
            y = value_chain[1]
            z = value_chain[2]
            print(x1)
            x2 = lambda x: (x1**2)/2

            dis = integrate.cumtrapz()
            print(dis)
            dis1=dis1+dis
            print("displacement=",dis1)
            i+=1
            if i == 10:
                self.ser.flushInput()
        else:
            print(len(value_chain))
            print(value_chain)
            print("faulty value")
        # try:
        #     ## store previous data in variable to use when error data is received from serial port
        #
        #     if len(value_chain) != 0:
        #         self.ser.flushInput()
        #         print(value_chain)
        #         # result1 = integrate.quad(value_chain[0], 0, 1)
        #         # print('Result is ', result1)
        #         return value_chain
        #
        # except:
        #     self.ser.flushInput()


com = Communication()
while 1:
    time.sleep(0.01)
    value_chain = com.getData()

    # try:
    #     result1 = integrate.quad(value_chain[0], 0, 1)
    #     result2 = integrate.quad(result1[0], 0, 1)
    #
    #     print('Result is ', result2)
    # except:
    #     print("error")