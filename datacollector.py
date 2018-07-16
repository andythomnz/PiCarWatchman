
 
import os
from gps import *
from time import *
from pytz import timezone
from datetime import datetime
import time
import threading
import obd
import math
import sqlite3
import requests
 
gpsd = None
obdConnection = obd.OBD("/dev/ttyUSB5")
db = sqlite3.connect('mydb')
 
class PiCarWatchmanGPS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True
 
    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
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
                      `obd_fuel_status` INTEGER
                    )
                       ''')
    db.commit()
    
    gpsp = PiCarWatchmanGPS() # create the GPS thread
    try:
        gpsp.start() # start the GPS thread
        while True:
            os.system('clear')
            
            florida = timezone('US/Eastern')
            now = datetime.now(florida).strftime('%Y-%m-%d %H:%M:%S')
            print("Current TimeStamp: " + str(now))

            #print
            #print ' GPS reading'
            #print '----------------------------------------'
            #print 'latitude    ' , gpsd.fix.latitude
            #print 'longitude   ' , gpsd.fix.longitude
            #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
            #print 'altitude (m)' , gpsd.fix.altitude
            #print 'eps         ' , gpsd.fix.eps
            #print 'epx         ' , gpsd.fix.epx
            #print 'epv         ' , gpsd.fix.epv
            #print 'ept         ' , gpsd.fix.ept
            #print 'speed (m/s) ' , gpsd.fix.speed
            #print 'climb       ' , gpsd.fix.climb
            #print 'track       ' , gpsd.fix.track
            #print 'mode        ' , gpsd.fix.mode
            #print
            #print 'sats        ' , gpsd.satellites
            
            latitude = 123456789
            if gpsd.fix.latitude != 0:
                latitude = gpsd.fix.latitude
            print("Latitude: " + str(latitude))
            
            longitude = 123456789
            if gpsd.fix.longitude != 0:
                longitude = gpsd.fix.longitude
            print("Longitude: " + str(longitude))   
        
            altitude = -123456789
            if not(math.isnan(gpsd.fix.altitude)):
                altitude = gpsd.fix.altitude
            print("Altitude: " + str(altitude))
            
            speed = -1
            if not(math.isnan(gpsd.fix.speed)):
                speed = (gpsd.fix.speed * 18)/5 #converting to km/h
            print("GPS Speed: " + str(speed))
                
            #OBD Data
            
            voltageCmd = obd.commands.ELM_VOLTAGE
            voltageRsp = obdConnection.query(voltageCmd)
            try:
                voltageValue = voltageRsp.value.magnitude
            except:
                voltageValue = -1
            print("Voltage: " + str(voltageValue))
            
            speedCmd = obd.commands.SPEED
            speedRsp = obdConnection.query(speedCmd)
            try:
                speedValue = speedRsp.value.magnitude
            except:
                speedValue = -1
            print("Speed: " + str(speedValue))

            distanceClrCmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
            distanceClrRsp = obdConnection.query(distanceClrCmd)
            try:
                distanceClrValue = distanceClrRsp.value.magnitude
            except:
                distanceClrValue = -1
            print("Distance since DTCs cleared: " + str(distanceClrValue))

            coolantTempCmd = obd.commands.COOLANT_TEMP
            coolantTempRsp = obdConnection.query(coolantTempCmd)
            try:
                coolantTempValue = coolantTempRsp.value.magnitude
            except:
                coolantTempValue = -1
            print("Coolant Temperature: " + str(coolantTempValue))

            relThrottlePosCmd = obd.commands.RELATIVE_THROTTLE_POS
            relThrottlePosRsp = obdConnection.query(relThrottlePosCmd)
            try:
                relThrottlePosValue = relThrottlePosRsp.value.magnitude
            except:
                relThrottlePosValue = -1
            print("Relative Throttle Position: " + str(relThrottlePosValue))

            ambientAirTempCmd = obd.commands.AMBIANT_AIR_TEMP
            ambientAirTempRsp = obdConnection.query(ambientAirTempCmd)
            try:
                ambientAirTempValue = ambientAirTempRsp.value.magnitude
            except:
                ambientAirTempValue = -1
            print("Ambient Air Temperature: " + str(ambientAirTempValue))

            ltftCmd = obd.commands.LONG_FUEL_TRIM_1
            ltftRsp = obdConnection.query(ltftCmd)
            try:
                ltftValue = lftfRsp.value.magnitude
            except:
                ltftValue = -1
            print("Long term fuel trim: " + str(ltftValue))

            stftCmd = obd.commands.SHORT_FUEL_TRIM_1
            stftRsp = obdConnection.query(stftCmd)
            try:
                stftValue = stftRsp.value.magnitude
            except:
                stftValue = -1
            print("Short term fuel trim: " + str(stftValue))

            intakeTempCmd = obd.commands.INTAKE_TEMP
            intakeTempRsp = obdConnection.query(intakeTempCmd)
            try:
                intakeTempValue = intakeTempRsp.value.magnitude
            except:
                intakeTempValue = -1
            print("Intake temperature: " + str(intakeTempValue))

            intakePressCmd = obd.commands.INTAKE_PRESSURE
            intakePressRsp = obdConnection.query(intakePressCmd)
            try:
                intakePressValue = intakePressRsp.value.magnitude
            except:
                intakePressValue = -1
            print("Intake pressure: " + str(intakePressValue))

            engineLoadCmd = obd.commands.ENGINE_LOAD
            engineLoadRsp = obdConnection.query(engineLoadCmd)
            try:
                engineLoadValue = engineLoadRsp.value.magnitude
            except:
                engineLoadValue = -1
            print("Engine load: " + str(engineLoadValue))

            rpmCmd = obd.commands.RPM
            rpmRsp = obdConnection.query(rpmCmd)
            try:
                rpmValue = rpmRsp.value.magnitude
            except:
                rpmValue = -1
            print("RPM: " + str(rpmValue))

            statusCmd = obd.commands.STATUS
            statusRsp = obdConnection.query(statusCmd)
            try:
                milValue = statusRsp.value.MIL
                dtcCountValue = statusRsp.value.DTC_count
            except:
                milValue = -1
                dtcCountValue = -1
            print("MIL Iluminated: " + str(milValue))
            print("Stored DTCs: " + str(dtcCountValue))

            getDtcCmd = obd.commands.GET_DTC
            getDtcRsp = obdConnection.query(getDtcCmd)
            try:
                dtcText = getDtcRsp.value
            except:
                dtcText = "Unable to communicate with vehicle"
            print("Summary of DTCs: " + str(dtcText))

            runTimeCmd = obd.commands.RUN_TIME
            runTimeRsp = obdConnection.query(runTimeCmd)
            try:
                runTimeValue = runTimeRsp.value.magnitude
            except:
                runTimeValue = -1
            print("Runtime: " + str(runTimeValue))

            fuelStatusCmd = obd.commands.FUEL_STATUS
            fuelStatusRsp = obdConnection.query(fuelStatusCmd)
            try:
                #fuelStatusValue = str(fuelStatusRsp.value[0])
                fuelStatusValue = "hi"
            except:
                fuelStatusValue = "Unable to communicate with vehicle"
            if fuelStatusValue == None:
                    fuelStatusValue = "Unavailable"
            print("Fuel System Status: " + str(fuelStatusValue))
            
            acc = False
            if speedValue > -1:
                acc = true
            
            #Add to local database
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
                                                    obd_fuel_status)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                                                    
                                                    now,                    # row[1]
                                                    acc,                    # row[2]
                                                    voltageValue,           # row[3]
                                                    latitude,               # row[4]
                                                    longitude,              # row[5]
                                                    altitude,               # row[6]
                                                    speed,                  # row[7]
                                                    speedValue,             # row[8]
                                                    distanceClrValue,       # row[9]
                                                    coolantTempValue,       # row[10]
                                                    relThrottlePosValue,    # row[11]
                                                    ambientAirTempValue,    # row[12]
                                                    ltftValue,              # row[13]
                                                    stftValue,              # row[14]
                                                    intakeTempValue,        # row[15]
                                                    intakePressValue,       # row[16]
                                                    engineLoadValue,        # row[17]
                                                    rpmValue,               # row[18]
                                                    milValue,               # row[19]
                                                    dtcCountValue,          # row[20]
                                                    dtcText,                # row[21]
                                                    runTimeValue,           # row[22]
                                                    fuelStatusValue))       # row[23]
            db.commit()


            #Try to upload local database to remote database
            print("Begin uploading local database to remote database")

            cursor.execute('''SELECT * FROM car_data''')
            allRecords = cursor.fetchall()
            for row in allRecords:
                # row[0] returns the first column in the query (id), row[1] returns the 'now' column
                url = ("http://www.mgt.co.nz/picarwatchman/newcardata.php?"
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
                       + "obd_fuel_status=" + str(row[23]))

                print("URL formed as: " + url)

                #make http request using URL and capture the HTTP status code
                r = requests.get(url)
                print("Status Code: " + str(r.status_code))

                #if successful, remove the row from the local database
                if str(r.status_code).startswith('2'):
                    print("Upload Success!")
                    cursor.execute('''DELETE FROM car_data WHERE id = ? ''',(row[0],))
                    db.commit()

            
            #Pause for a few seconds before repeating
            time.sleep(10) #set to whatever
 
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        db.close()
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing
        print "Done.\nExiting."