# dataManager.py:

import sqlite3
import requests
import threading
from config import *

db = sqlite3.connect(databasePath)
cursor = db.cursor()


class DataManager(threading.Thread):

    def __init__(self):
        global cursor
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True
        # prepare the database
        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS `car_data` (
                              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                              `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
                              `acc` tinyint(1) DEFAULT NULL,
                              `voltage` double DEFAULT NULL,
                              `latitude` double DEFAULT NULL,
                              `latitude_error` double DEFAULT NULL,
                              `longitude` double DEFAULT NULL,
                              `longitude_error` double DEFAULT NULL,
                              `altitude` double DEFAULT NULL,
                              `altitude_error` double DEFAULT NULL,
                              `speed` double DEFAULT NULL,
                              `speed_error` double DEFAULT NULL,
                              `heading` double DEFAULT NULL,
                              `heading_error` double DEFAULT NULL,
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

    def run(self):
        while self.running:
            # upload data
            new_db = sqlite3.connect(databasePath)
            new_cursor = new_db.cursor()
            new_cursor.execute('''SELECT * FROM car_data ORDER BY created DESC LIMIT 5''')
            all_records = new_cursor.fetchall()
            if all_records:  # if all_records is not empty
                print("Beginning to upload " + str(len(all_records)) + " data rows...")
                # print("The data rows are: " + str(all_records))
                self.upload(all_records, new_cursor, new_db)
                print("Upload attempts finished")


    def add(self,
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
            speedValue,
            distanceClrValue,
            coolantTempValue,
            relThrottlePosValue,
            ambientAirTempValue,
            ltftValue,
            stftValue,
            intakeTempValue,
            intakePressValue,
            engineLoadValue,
            rpmValue,
            milValue,
            dtcCountValue,
            dtcText,
            runTimeValue,
            fuelStatusValue,
            softwareVersion
            ):
        global cursor
        cursor.execute('''INSERT INTO car_data(
                                                            created, 
                                                            acc, 
                                                            voltage, 
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
                          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (

            now,  # row[1]
            acc,  # row[2]
            voltageValue,  # row[3]
            latitude,  # row[4]
            latitude_error,  # row[5]
            longitude,  # row[6]
            longitude_error,  # row[7]
            altitude,  # row[8]
            altitude_error,  # row[9]
            speed,  # row[10]
            speed_error,  # row[11]
            heading,  # row[12]
            heading_error,  # row[13]
            speedValue,  # row[14]
            distanceClrValue,  # row[15]
            coolantTempValue,  # row[16]
            relThrottlePosValue,  # row[17]
            ambientAirTempValue,  # row[18]
            ltftValue,  # row[19]
            stftValue,  # row[20]
            intakeTempValue,  # row[21]
            intakePressValue,  # row[22]
            engineLoadValue,  # row[23]
            rpmValue,  # row[24]
            milValue,  # row[25]
            dtcCountValue,  # row[26]
            dtcText,  # row[27]
            runTimeValue,  # row[28]
            fuelStatusValue,  # row[29]
            softwareVersion  # row[30]
        ))
        db.commit()

    def get_num_cached(self):
        global cursor
        cursor.execute('''SELECT Count(*) FROM car_data''')
        num_cached = cursor.fetchone()
        num_cached = num_cached[0]
        return num_cached

    def upload(self, allRecords, new_cursor, new_db):
        # new_cursor = db.cursor()
        # new_cursor.execute('''SELECT * FROM car_data''')
        # allRecords = new_cursor.fetchall()
        for row in allRecords:
            # row[0] returns the first column in the query (id), row[1] returns the 'now' column
            url = (databaseConnection + "?"
                   + "created=" + str(row[1]) + "&"
                   + "acc=" + str(row[2]) + "&"
                   + "voltage=" + str(row[3]) + "&"
                   + "latitude=" + str(row[4]) + "&"
                   + "latitude_error=" + str(row[5]) + "&"
                   + "longitude=" + str(row[6]) + "&"
                   + "longitude_error=" + str(row[7]) + "&"
                   + "altitude=" + str(row[8]) + "&"
                   + "altitude_error=" + str(row[9]) + "&"
                   + "speed=" + str(row[10]) + "&"
                   + "speed_error=" + str(row[11]) + "&"
                   + "heading=" + str(row[12]) + "&"
                   + "heading_error=" + str(row[13]) + "&"
                   + "obd_speed=" + str(row[14]) + "&"
                   + "obd_dtc_reset_dist=" + str(row[15]) + "&"
                   + "obd_coolant_temp=" + str(row[16]) + "&"
                   + "obd_rel_throttle_pos=" + str(row[17]) + "&"
                   + "obd_ambient_air_temp=" + str(row[18]) + "&"
                   + "obd_ltft=" + str(row[19]) + "&"
                   + "obd_stft=" + str(row[20]) + "&"
                   + "obd_intake_air_temp=" + str(row[21]) + "&"
                   + "obd_intake_man_pressure=" + str(row[22]) + "&"
                   + "obd_engine_load=" + str(row[23]) + "&"
                   + "obd_rpm=" + str(row[24]) + "&"
                   + "obd_MIL=" + str(row[25]) + "&"
                   + "obd_dtc_count=" + str(row[26]) + "&"
                   + "obd_dtc_info=" + str(row[27]) + "&"
                   + "obd_engine_runtime=" + str(row[28]) + "&"
                   + "obd_fuel_status=" + str(row[29]) + "&"
                   + "software_version=" + str(row[30]))

            # print("URL formed as: " + url)

            # make http request using URL and capture the HTTP status code
            r = requests.get(url)
            print("Status Code: " + str(r.status_code))

            # if successful, remove the row from the local database
            if str(r.status_code).startswith('2'):
                # print("Upload Success!")
                new_cursor.execute('''DELETE FROM car_data WHERE id = ? ''', (row[0],))
                new_db.commit()

            # if not successful, don't try uploading the rest of the list
            if not(str(r.status_code).startswith('2')):
                print("Error uploading to database!")
                break
