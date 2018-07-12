
 
import os
from gps import *
from time import *
import time
import threading
import obd
 
gpsd = None
obdConnection = obd.OBD("/dev/ttyUSB5")
 
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
    gpsp = PiCarWatchmanGPS() # create the GPS thread
    try:
        gpsp.start() # start the GPS thread
        while True:
            os.system('clear')
            
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            print("Current TimeStamp: " + str(now))

            print
            print ' GPS reading'
            print '----------------------------------------'
            print 'latitude    ' , gpsd.fix.latitude
            print 'longitude   ' , gpsd.fix.longitude
            print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
            print 'altitude (m)' , gpsd.fix.altitude
            print 'eps         ' , gpsd.fix.eps
            print 'epx         ' , gpsd.fix.epx
            print 'epv         ' , gpsd.fix.epv
            print 'ept         ' , gpsd.fix.ept
            print 'speed (m/s) ' , gpsd.fix.speed
            print 'climb       ' , gpsd.fix.climb
            print 'track       ' , gpsd.fix.track
            print 'mode        ' , gpsd.fix.mode
            print
            print 'sats        ' , gpsd.satellites

            #OBD Data
            
            speedCmd = obd.commands.SPEED
            speedRsp = connection.query(speedCmd)
            print("Speed: " + str(speedRsp.value.magnitude))

            distanceClrCmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
            distanceClrRsp = connection.query(distanceClrCmd)
            print("Distance since DTCs cleared: " + str(distanceClrRsp.value.magnitude))

            coolantTempCmd = obd.commands.COOLANT_TEMP
            coolantTempRsp = connection.query(coolantTempCmd)
            print("Coolant Temperature: " + str(coolantTempRsp.value.magnitude))

            relThrottlePosCmd = obd.commands.RELATIVE_THROTTLE_POS
            relThrottlePosRsp = connection.query(relThrottlePosCmd)
            print("Relative Throttle Position: " + str(relThrottlePosRsp.value.magnitude))

            ambientAirTempCmd = obd.commands.AMBIANT_AIR_TEMP
            ambientAirTempRsp = connection.query(ambientAirTempCmd)
            print("Ambient Air Temperature: " + str(ambientAirTempRsp.value.magnitude))

            ltftCmd = obd.commands.LONG_FUEL_TRIM_1
            ltftRsp = connection.query(ltftCmd)
            print("Long term fuel trim: " + str(ltftRsp.value.magnitude))

            stftCmd = obd.commands.SHORT_FUEL_TRIM_1
            stftRsp = connection.query(stftCmd)
            print("Short term fuel trim: " + str(stftRsp.value.magnitude))

            intakeTempCmd = obd.commands.INTAKE_TEMP
            intakeTempRsp = connection.query(intakeTempCmd)
            print("Intake temperature: " + str(intakeTempRsp.value.magnitude))

            intakePressCmd = obd.commands.INTAKE_PRESSURE
            intakePressRsp = connection.query(intakePressCmd)
            print("Intake pressure: " + str(intakePressRsp.value.magnitude))

            engineLoadCmd = obd.commands.ENGINE_LOAD
            engineLoadRsp = connection.query(engineLoadCmd)
            print("Engine load: " + str(engineLoadRsp.value.magnitude))

            rpmCmd = obd.commands.RPM
            rpmRsp = connection.query(rpmCmd)
            print("RPM: " + str(rpmRsp.value.magnitude))

            statusCmd = obd.commands.STATUS
            statusRsp = connection.query(statusCmd)
            print("MIL Iluminated: " + str(statusRsp.value.MIL))
            print("Stored DTCs: " + str(statusRsp.value.DTC_count))

            getDtcCmd = obd.commands.GET_DTC
            getDtcRsp = connection.query(getDtcCmd)
            print("Summary of DTCs: " + str(getDtcRsp.value))

            runTimeCmd = obd.commands.RUN_TIME
            runTimeRsp = connection.query(runTimeCmd)
            print("Runtime: " + str(runTimeRsp.value.magnitude))

            fuelStatusCmd = obd.commands.FUEL_STATUS
            fuelStatusRsp = connection.query(fuelStatusCmd)
            print("Fuel System Status: " + str(fuelStatusRsp.value))

            time.sleep(10) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    print "Done.\nExiting."