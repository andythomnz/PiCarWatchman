# datacollector.py:

from pytz import timezone
from datetime import datetime
from config import *
from obdData import *
from gpsData import *
from modemData import *
from dataManager import *
import os
import time
import obd

softwareVersion = 1.25

obdConnection = obd.OBD("/dev/ttyUSB1")

gpsDataWatcher = GpsDataWatcher()   # create the GPS thread
obdDataWatcher = ObdDataWatcher(obdConnection)  # create the OBD data thread
modemDataWatcher = ModemDataWatcher()   # create the modem data thread
dataManager = DataManager()     # instantiate the data manager


if __name__ == '__main__':

    global gpsDataWatcher
    global obdDataWatcher
    global modemDataWatcher
    global dataManager

    try:
        gpsDataWatcher.start()  # start the GPS data thread
        obdDataWatcher.start()  # start the OBD data thread
        modemDataWatcher.start()    # start the modem data thread
        dataManager.start()     # start the data manager thread

        while True:
            os.system('clear')

            print("Software Version: " + str(softwareVersion))

            print("Received Signal Strength: " + str(modemDataWatcher.received_signal_strength))

            print("Data Rows Awaiting Upload: " + str(dataManager.get_num_cached()))

            florida = timezone('US/Eastern')
            now = datetime.now(florida).strftime('%Y-%m-%d %H:%M:%S')
            print("Current TimeStamp: " + str(now))

            latitude = gpsDataWatcher.get_latitude()
            print("Latitude: " + str(latitude))

            latitude_error = gpsDataWatcher.get_latitude_error()
            print("Latitude Error: " + str(latitude_error) + " metres")

            longitude = gpsDataWatcher.get_longitude()
            print("Longitude: " + str(longitude))

            longitude_error = gpsDataWatcher.get_longitude_error()
            print("Longitude Error: " + str(longitude_error) + " metres")

            altitude = gpsDataWatcher.get_altitude()
            print("Altitude: " + str(altitude) + " metres")

            altitude_error = gpsDataWatcher.get_altitude_error()
            print("Altitude Error: " + str(altitude_error) + " metres")

            speed = gpsDataWatcher.get_speed()
            print("GPS Speed: " + str(speed) + " km/h")

            speed_error = gpsDataWatcher.get_speed_error()
            print("GPS Speed Error: " + str(speed_error) + " km/h")

            heading = gpsDataWatcher.get_heading()
            print("Heading: " + str(heading) + " degrees")

            heading_error = gpsDataWatcher.get_heading_error()
            print("Heading Error: " + str(heading_error) + " degrees")

            utc = gpsDataWatcher.get_utc()
            print("GPS UTC: " + str(utc))

            gps_timestamp = gpsDataWatcher.get_time()
            print("GPS Timestamp: " + str(gps_timestamp))

            # OBD Data

            # voltageCmd = obd.commands.ELM_VOLTAGE
            # voltageRsp = obdConnection.query(voltageCmd)
            # try:
            #    voltageValue = voltageRsp.value.magnitude
            # except:
            #    voltageValue = -1
            voltageValue = -1

            print("Voltage: " + str(voltageValue))
            print("Speed: " + str(obdDataWatcher.speedValue))
            print("Distance since DTCs cleared: " + str(obdDataWatcher.distanceClrValue))
            print("Coolant Temperature: " + str(obdDataWatcher.coolantTempValue))
            print("Relative Throttle Position: " + str(obdDataWatcher.relThrottlePosValue))
            print("Ambient Air Temperature: " + str(obdDataWatcher.ambientAirTempValue))
            print("Long term fuel trim: " + str(obdDataWatcher.ltftValue))
            print("Short term fuel trim: " + str(obdDataWatcher.stftValue))
            print("Intake temperature: " + str(obdDataWatcher.intakeTempValue))
            print("Intake pressure: " + str(obdDataWatcher.intakePressValue))
            print("Engine load: " + str(obdDataWatcher.engineLoadValue))
            print("RPM: " + str(obdDataWatcher.rpmValue))
            print("MIL Iluminated: " + str(obdDataWatcher.milValue))
            print("Stored DTCs: " + str(obdDataWatcher.dtcCountValue))
            print("Summary of DTCs: " + str(obdDataWatcher.dtcText))
            print("Runtime: " + str(obdDataWatcher.runTimeValue))
            print("Fuel System Status: " + str(obdDataWatcher.fuelStatusValue))

            acc = False
            if obdDataWatcher.speedValue > -1:
                acc = True

            # Add to local database
            print("Begin to add data record to local database")

            dataManager.add(
                now,
                acc,
                voltageValue,
                latitude,
                latitude_error,
                longitude,
                longitude_error,
                altitude,
                altitude_error,
                speed,
                speed_error,
                heading,
                heading_error,
                obdDataWatcher.speedValue,
                obdDataWatcher.distanceClrValue,
                obdDataWatcher.coolantTempValue,
                obdDataWatcher.relThrottlePosValue,
                obdDataWatcher.ambientAirTempValue,
                obdDataWatcher.ltftValue,
                obdDataWatcher.stftValue,
                obdDataWatcher.intakeTempValue,
                obdDataWatcher.intakePressValue,
                obdDataWatcher.engineLoadValue,
                obdDataWatcher.rpmValue,
                obdDataWatcher.milValue,
                obdDataWatcher.dtcCountValue,
                obdDataWatcher.dtcText,
                obdDataWatcher.runTimeValue,
                obdDataWatcher.fuelStatusValue,
                softwareVersion,
                modemDataWatcher.received_signal_strength
            )

            # Pause for a few seconds before repeating
            time.sleep(15)  # set to whatever

    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c

        print "\nKilling Threads..."
        db.close()
        gpsDataWatcher.running = False
        gpsDataWatcher.join()   # wait for GPS thread to finish
        obdDataWatcher.running = False
        obdDataWatcher.join()   # wait for OBD thread to finish

        print "Done.\nExiting."
