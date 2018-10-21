# obdData.py:

import obd
import threading
import time


class ObdDataWatcher(threading.Thread):
    obd.logger.removeHandler(obd.console_handler)  # silences console output from OBD library

    speedValue = -1
    distanceClrValue = -1
    coolantTempValue = -1
    relThrottlePosValue = -1
    ambientAirTempValue = -1
    ltftValue = -1
    stftValue = -1
    intakeTempValue = -1
    intakePressValue = -1
    engineLoadValue = -1
    rpmValue = -1
    milValue = -1
    dtcCountValue = -1
    dtcText = "Unable to communicate with vehicle"
    runTimeValue = -1
    fuelStatusValue = "Unable to communicate with vehicle"

    obdConnection = ""

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True
        global obdConnection
        obdConnection = device

    def run(self):
        global speedValue
        global distanceClrValue
        global coolantTempValue
        global relThrottlePosValue
        global ambientAirTempValue
        global ltftValue
        global stftValue
        global intakeTempValue
        global intakePressValue
        global engineLoadValue
        global rpmValue
        global milValue
        global dtcCountValue
        global dtcText
        global runTimeValue
        global fuelStatusValue

        while self.running:
            speedCmd = obd.commands.SPEED
            speedRsp = obdConnection.query(speedCmd)
            try:
                speedValue = speedRsp.value.magnitude
            except:
                speedValue = -1

            distanceClrCmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
            distanceClrRsp = obdConnection.query(distanceClrCmd)
            try:
                distanceClrValue = distanceClrRsp.value.magnitude
            except:
                distanceClrValue = -1

            coolantTempCmd = obd.commands.COOLANT_TEMP
            coolantTempRsp = obdConnection.query(coolantTempCmd)
            try:
                coolantTempValue = coolantTempRsp.value.magnitude
            except:
                coolantTempValue = -1

            relThrottlePosCmd = obd.commands.RELATIVE_THROTTLE_POS
            relThrottlePosRsp = obdConnection.query(relThrottlePosCmd)
            try:
                relThrottlePosValue = relThrottlePosRsp.value.magnitude
            except:
                relThrottlePosValue = -1

            ambientAirTempCmd = obd.commands.AMBIANT_AIR_TEMP
            ambientAirTempRsp = obdConnection.query(ambientAirTempCmd)
            try:
                ambientAirTempValue = ambientAirTempRsp.value.magnitude
            except:
                ambientAirTempValue = -1

            ltftCmd = obd.commands.LONG_FUEL_TRIM_1
            ltftRsp = obdConnection.query(ltftCmd)
            try:
                ltftValue = ltftRsp.value.magnitude
            except:
                ltftValue = -1

            stftCmd = obd.commands.SHORT_FUEL_TRIM_1
            stftRsp = obdConnection.query(stftCmd)
            try:
                stftValue = stftRsp.value.magnitude
            except:
                stftValue = -1

            intakeTempCmd = obd.commands.INTAKE_TEMP
            intakeTempRsp = obdConnection.query(intakeTempCmd)
            try:
                intakeTempValue = intakeTempRsp.value.magnitude
            except:
                intakeTempValue = -1

            intakePressCmd = obd.commands.INTAKE_PRESSURE
            intakePressRsp = obdConnection.query(intakePressCmd)
            try:
                intakePressValue = intakePressRsp.value.magnitude
            except:
                intakePressValue = -1

            engineLoadCmd = obd.commands.ENGINE_LOAD
            engineLoadRsp = obdConnection.query(engineLoadCmd)
            try:
                engineLoadValue = engineLoadRsp.value.magnitude
            except:
                engineLoadValue = -1

            rpmCmd = obd.commands.RPM
            rpmRsp = obdConnection.query(rpmCmd)
            try:
                rpmValue = rpmRsp.value.magnitude
            except:
                rpmValue = -1

            statusCmd = obd.commands.STATUS
            statusRsp = obdConnection.query(statusCmd)
            try:
                milValue = statusRsp.value.MIL
                dtcCountValue = statusRsp.value.DTC_count
            except:
                milValue = -1
                dtcCountValue = -1

            getDtcCmd = obd.commands.GET_DTC
            getDtcRsp = obdConnection.query(getDtcCmd)
            try:
                dtcList = getDtcRsp.value
                dtcText = ','.join(map(str, dtcList))
            except:
                dtcText = "Unable to communicate with vehicle"

            runTimeCmd = obd.commands.RUN_TIME
            runTimeRsp = obdConnection.query(runTimeCmd)
            try:
                runTimeValue = runTimeRsp.value.magnitude
            except:
                runTimeValue = -1

            fuelStatusCmd = obd.commands.FUEL_STATUS
            fuelStatusRsp = obdConnection.query(fuelStatusCmd)
            try:
                fuelStatusValue = str(fuelStatusRsp.value[0])
            except:
                fuelStatusValue = "Unable to communicate with vehicle"
            if fuelStatusValue is None:
                fuelStatusValue = "Unavailable"

            # Pause for a few seconds before repeating
            time.sleep(1)  # set to whatever
