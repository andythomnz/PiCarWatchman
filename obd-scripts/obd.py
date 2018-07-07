import obd

connection = obd.OBD("/dev/ttyUSB0")

try:
    
    while True:
        
        os.system('clear') #clear the terminal

        speedCmd = obd.commands.SPEED
        speedRsp = connection.query(speedCmd)
        print("Speed: " + speedRsp.value)

        distanceClrCmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
        distanceClrRsp = connection.query(distanceClrCmd)
        print("Distance since DTCs cleared: " + distanceClrRsp.value)

        coolantTempCmd = obd.commands.COOLANT_TEMP
        coolantTempRsp = connection.query(coolantTempCmd)
        print("Coolant Temperature: " + coolantTempRsp.value)

        relThrottlePosCmd = obd.commands.RELATIVE_THROTTLE_POS
        relThrottlePosRsp = connection.query(relThrottlePosCmd)
        print("Relative Throttle Position: " + relThrottlePosRsp.value)

        ambientAirTempCmd = obd.commands.AMBIANT_AIR_TEMP
        ambientAirTempRsp = connection.query(ambientAirTempCmd)
        print("Ambient Air Temperature: " + ambientAirTempRsp.value)

        ltftCmd = obd.commands.LONG_FUEL_TRIM_1
        ltftRsp = connection.query(ltftCmd)
        print("Long term fuel trim: " + ltftRsp.value)

        stftCmd = obd.commands.SHORT_FUEL_TRIM_1
        stftRsp = connection.query(stftCmd)
        print("Short term fuel trim: " + stftRsp.value)

        intakeTempCmd = obd.commands.INTAKE_TEMP
        intakeTempRsp = connection.query(intakeTempCmd)
        print("Intake temperature: " + intakeTempRsp.value)
        
        time.sleep(5)
    
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("Exiting...")