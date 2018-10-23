# modemData.py:

import serial
import threading
import time
from config import *


class ModemDataWatcher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True
        self.received_signal_strength = -1

    def run(self):

        while self.running:
            ser = serial.Serial(modemDevice, 9600, timeout=2)

            at_command = 'AT+CSQ\r\n'
            ser.write(at_command)
            ser.sendBreak()

            line = ser.read(ser.inWaiting())
            ser.close

            try:
                comma = line.find(',')
                if comma > -1:
                    self.received_signal_strength = line[comma - 2:comma]
            except:
                self.received_signal_strength = -1

            # Pause for a few seconds before repeating
            time.sleep(10)  # set to whatever
