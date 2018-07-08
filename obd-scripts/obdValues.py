import os
import time
import obd

#obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD("/dev/ttyUSB5")
#connection = obd.OBD()

try:
    
    while True:
        
        os.system('clear') #clear the terminal

        speedCmd = obd.commands.SPEED
        speedRsp = connection.query(speedCmd)
        print("Speed: " + str(speedRsp.value))

        distanceClrCmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
        distanceClrRsp = connection.query(distanceClrCmd)
        print("Distance since DTCs cleared: " + str(distanceClrRsp.value))

        coolantTempCmd = obd.commands.COOLANT_TEMP
        coolantTempRsp = connection.query(coolantTempCmd)
        print("Coolant Temperature: " + str(coolantTempRsp.value))

        relThrottlePosCmd = obd.commands.RELATIVE_THROTTLE_POS
        relThrottlePosRsp = connection.query(relThrottlePosCmd)
        print("Relative Throttle Position: " + str(relThrottlePosRsp.value))

        ambientAirTempCmd = obd.commands.AMBIANT_AIR_TEMP
        ambientAirTempRsp = connection.query(ambientAirTempCmd)
        print("Ambient Air Temperature: " + str(ambientAirTempRsp.value))

        ltftCmd = obd.commands.LONG_FUEL_TRIM_1
        ltftRsp = connection.query(ltftCmd)
        print("Long term fuel trim: " + str(ltftRsp.value))

        stftCmd = obd.commands.SHORT_FUEL_TRIM_1
        stftRsp = connection.query(stftCmd)
        print("Short term fuel trim: " + str(stftRsp.value))

        intakeTempCmd = obd.commands.INTAKE_TEMP
        intakeTempRsp = connection.query(intakeTempCmd)
        print("Intake temperature: " + str(intakeTempRsp.value))
        
        intakePressCmd = obd.commands.INTAKE_PRESSURE
        intakePressRsp = connection.query(intakePressCmd)
        print("Intake pressure: " + str(intakePressRsp.value))
        
        engineLoadCmd = obd.commands.ENGINE_LOAD
        engineLoadRsp = connection.query(engineLoadCmd)
        print("Engine load: " + str(engineLoadRsp.value))
        
        rpmCmd = obd.commands.RPM
        rpmRsp = connection.query(rpmCmd)
        print("RPM: " + str(rpmRsp.value))
        
        statusCmd = obd.commands.STATUS
        statusRsp = connection.query(statusCmd)
        print("MIL Iluminated: " + str(statusRsp.value.MIL))
        print("Stored DTCs: " + str(statusRsp.value.DTC_count))
        
        getDtcCmd = obd.commands.GET_DTC
        getDtcRsp = connection.query(getDtcCmd)
        print("Summary of DTCs: " + str(getDtcRsp.value))
        
        runTimeCmd = obd.commands.RUN_TIME
        runTimeRsp = connection.query(runTimeCmd)
        print("Runtime: " + str(runTimeRsp.value))
        
        fuelStatusCmd = obd.commands.FUEL_STATUS
        fuelStatusRsp = connection.query(fuelStatusCmd)
        print("Fuel System Status: " + str(fuelStatusRsp.value))
        
        time.sleep(5)
    
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("Exiting...")