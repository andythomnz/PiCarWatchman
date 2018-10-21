import os
# from gps import *
from pytz import timezone
from datetime import datetime
from config import *
from obdData import *
from gpsData import *
import time
# import threading
import obd
# import math
import sqlite3
import requests

softwareVersion = 1.13

# gpsd = None
obdConnection = obd.OBD("/dev/ttyUSB1")
db = sqlite3.connect('/home/pi/PiCarWatchman/src/database')


# class PiCarWatchmanGPS(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         global gpsd
#         gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
#         self.current_value = None
#         self.running = True
#
#     def run(self):
#         global gpsd
#         while gpsp.running:
#             gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer


if __name__ == '__main__':

    # prepare the database
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS `car_data` (
                      `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
                      `acc` tinyint(1) DEFAULT NULL,
                      `voltage` double DEFAULT NULL,
                      `latitude` double DEFAULT NULL,
                      `longitude` double DEFAULT NULL,
                      `altitude` double DEFAULT NULL,
                      `speed` double DEFAULT NULL,
                      `obd_speed` double DEFAULT NULL,
                      `obd_dtc_reset_dist` int(11) DEFAULT NULL,
                      `obd_coolant_temp` int(11) DEFAULT NULL,
                      `obd_rel_throttle_pos` int(11) DEFAULT NULL,
                      `obd_ambient_air_temp` double DEFAULT NULL,
                      `obd_ltft` double DEFAULT NULL,
                      `obd_stft` double DEFAULT NULL,
                      `obd_intake_air_temp` double DEFAULT NULL,
                      `obd_intake_man_pressure` double DEFAULT NULL,
                      `obd_engine_load` double DEFAULT NULL,
                      `obd_rpm` int(11) DEFAULT NULL,
                      `obd_MIL` tinyint(1) DEFAULT NULL,
                      `obd_dtc_count` int(11) DEFAULT NULL,
                      `obd_dtc_info` longtext,
                      `obd_engine_runtime` int(11) NOT NULL,
                      `obd_fuel_status` INTEGER,
                      'software_version' double DEFAULT NULL
                    )
                       ''')
    db.commit()

    # gpsp = PiCarWatchmanGPS()  # create the GPS thread
    gpsDataWatcher = GpsDataWatcher()   # create the GPS thread
    obdDataWatcher = ObdDataWatcher(obdConnection)  # create the OBD data thread

    try:
        # gpsp.start()  # start the GPS thread
        gpsDataWatcher.start()  # start the GPS data thread
        obdDataWatcher.start()  # start the OBD data thread

        while True:
            os.system('clear')

            florida = timezone('US/Eastern')
            now = datetime.now(florida).strftime('%Y-%m-%d %H:%M:%S')
            print("Current TimeStamp: " + str(now))

            # print
            # print ' GPS reading'
            # print '----------------------------------------'
            # print 'latitude    ' , gpsd.fix.latitude
            # print 'longitude   ' , gpsd.fix.longitude
            # print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
            # print 'altitude (m)' , gpsd.fix.altitude
            # print 'eps         ' , gpsd.fix.eps
            # print 'epx         ' , gpsd.fix.epx
            # print 'epv         ' , gpsd.fix.epv
            # print 'ept         ' , gpsd.fix.ept
            # print 'speed (m/s) ' , gpsd.fix.speed
            # print 'climb       ' , gpsd.fix.climb
            # print 'track       ' , gpsd.fix.track
            # print 'mode        ' , gpsd.fix.mode
            # print
            # print 'sats        ' , gpsd.satellites

            # latitude = 123456789
            # if gpsd.fix.latitude != 0:
            #     latitude = gpsd.fix.latitude
            latitude = gpsDataWatcher.get_latitude()
            print("Latitude: " + str(latitude))

            latitude_error = gpsDataWatcher.get_latitude_error()
            print("Latitude Error: " + str(latitude_error) + " metres")

            # longitude = 123456789
            # if gpsd.fix.longitude != 0:
            #     longitude = gpsd.fix.longitude
            longitude = gpsDataWatcher.get_longitude()
            print("Longitude: " + str(longitude))

            longitude_error = gpsDataWatcher.get_longitude_error()
            print("Longitude Error: " + str(longitude_error) + " metres")

            # altitude = -123456789
            # if not (math.isnan(gpsd.fix.altitude)):
            #     altitude = gpsd.fix.altitude
            altitude = gpsDataWatcher.get_altitude()
            print("Altitude: " + str(altitude) + " metres")

            altitude_error = gpsDataWatcher.get_altitude_error()
            print("Altitude Error: " + str(altitude_error) + " metres")

            # speed = -1
            # if not (math.isnan(gpsd.fix.speed)):
            #     speed = (gpsd.fix.speed * 18) / 5  # converting to km/h
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

            cursor.execute('''INSERT INTO car_data(
                                                    created, 
                                                    acc, 
                                                    voltage, 
                                                    latitude,
                                                    longitude,
                                                    altitude,
                                                    speed,
                                                    obd_speed,
                                                    obd_dtc_reset_dist,
                                                    obd_coolant_temp,
                                                    obd_rel_throttle_pos,
                                                    obd_ambient_air_temp,
                                                    obd_ltft,
                                                    obd_stft,
                                                    obd_intake_air_temp,
                                                    obd_intake_man_pressure,
                                                    obd_engine_load,
                                                    obd_rpm,
                                                    obd_MIL,
                                                    obd_dtc_count,
                                                    obd_dtc_info,
                                                    obd_engine_runtime,
                                                    obd_fuel_status,
                                                    software_version)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (

                now,  # row[1]
                acc,  # row[2]
                voltageValue,  # row[3]
                latitude,  # row[4]
                longitude,  # row[5]
                altitude,  # row[6]
                speed,  # row[7]
                obdDataWatcher.speedValue,  # row[8]
                obdDataWatcher.distanceClrValue,  # row[9]
                obdDataWatcher.coolantTempValue,  # row[10]
                obdDataWatcher.relThrottlePosValue,  # row[11]
                obdDataWatcher.ambientAirTempValue,  # row[12]
                obdDataWatcher.ltftValue,  # row[13]
                obdDataWatcher.stftValue,  # row[14]
                obdDataWatcher.intakeTempValue,  # row[15]
                obdDataWatcher.intakePressValue,  # row[16]
                obdDataWatcher.engineLoadValue,  # row[17]
                obdDataWatcher.rpmValue,  # row[18]
                obdDataWatcher.milValue,  # row[19]
                obdDataWatcher.dtcCountValue,  # row[20]
                obdDataWatcher.dtcText,  # row[21]
                obdDataWatcher.runTimeValue,  # row[22]
                obdDataWatcher.fuelStatusValue,  # row[23]
                softwareVersion))  # row[24]
            db.commit()

            # Try to upload local database to remote database
            print("Begin uploading local database to remote database")

            cursor.execute('''SELECT * FROM car_data''')
            allRecords = cursor.fetchall()
            for row in allRecords:
                # row[0] returns the first column in the query (id), row[1] returns the 'now' column
                url = (databaseConnection+"?"
                       + "created=" + str(row[1]) + "&"
                       + "acc=" + str(row[2]) + "&"
                       + "voltage=" + str(row[3]) + "&"
                       + "latitude=" + str(row[4]) + "&"
                       + "longitude=" + str(row[5]) + "&"
                       + "altitude=" + str(row[6]) + "&"
                       + "speed=" + str(row[7]) + "&"
                       + "obd_speed=" + str(row[8]) + "&"
                       + "obd_dtc_reset_dist=" + str(row[9]) + "&"
                       + "obd_coolant_temp=" + str(row[10]) + "&"
                       + "obd_rel_throttle_pos=" + str(row[11]) + "&"
                       + "obd_ambient_air_temp=" + str(row[12]) + "&"
                       + "obd_ltft=" + str(row[13]) + "&"
                       + "obd_stft=" + str(row[14]) + "&"
                       + "obd_intake_air_temp=" + str(row[15]) + "&"
                       + "obd_intake_man_pressure=" + str(row[16]) + "&"
                       + "obd_engine_load=" + str(row[17]) + "&"
                       + "obd_rpm=" + str(row[18]) + "&"
                       + "obd_MIL=" + str(row[19]) + "&"
                       + "obd_dtc_count=" + str(row[20]) + "&"
                       + "obd_dtc_info=" + str(row[21]) + "&"
                       + "obd_engine_runtime=" + str(row[22]) + "&"
                       + "obd_fuel_status=" + str(row[23]) + "&"
                       + "software_version=" + str(row[24]))

                print("URL formed as: " + url)

                # make http request using URL and capture the HTTP status code
                r = requests.get(url)
                print("Status Code: " + str(r.status_code))

                # if successful, remove the row from the local database
                if str(r.status_code).startswith('2'):
                    print("Upload Success!")
                    cursor.execute('''DELETE FROM car_data WHERE id = ? ''', (row[0],))
                    db.commit()

            # Pause for a few seconds before repeating
            time.sleep(5)  # set to whatever

    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print "\nKilling Thread..."
        db.close()
        gpsp.running = False
        gpsp.join()  # wait for the thread to finish what it's doing
        print "Done.\nExiting."
