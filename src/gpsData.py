# gpsData.py:

import threading
from gps import *


def is_nan(num):
    return num != num


class GpsDataWatcher(threading.Thread):

    data = None

    def __init__(self):
        threading.Thread.__init__(self)
        global data
        data = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True

    def run(self):
        global data
        while self.running:
            data.next()  # this will continue to loop grabbing each data set and clearing the GPS' buffer

    def get_latitude(self):
        latitude = -123456789
        if data.fix.latitude != 0 and (not(is_nan(data.fix.latitude))):
            latitude = data.fix.latitude
        return latitude

    def get_latitude_error(self):
        # in metres.
        # 95% chance that true latitude is within gps latitude plus or minus latitude_error
        latitude_error = -123456789
        if not(is_nan(data.fix.epy)):
            latitude_error = data.fix.epy
        return latitude_error

    def get_longitude(self):
        longitude = -123456789
        if data.fix.longitude != 0 and (not(is_nan(data.fix.longitude))):
            longitude = data.fix.longitude
        return longitude

    def get_longitude_error(self):
        # in metres.
        # 95% chance that true longitude is within gps longitude plus or minus longitude_error
        longitude_error = -123456789
        if not(is_nan(data.fix.epx)):
            longitude_error = data.fix.epx
        return longitude_error

    def get_altitude(self):
        # in metres.
        altitude = -123456789
        if not(is_nan(data.fix.altitude)):
            altitude = data.fix.altitude
        return altitude

    def get_altitude_error(self):
        # in metres.
        # 95% chance that true altitude is within gps altitude plus or minus altitude_error
        altitude_error = -123456789
        if not(is_nan(data.fix.epv)):
            altitude_error = data.fix.epv
        return altitude_error

    def get_speed(self):
        # in km/h.
        speed = -123456789
        if not(is_nan(data.fix.speed)):
            speed = data.fix.speed
            speed = speed * 18
            speed = speed / 5   # converting to km/h
        return speed

    def get_speed_error(self):
        # in km/h.
        # 95% chance that true speed is within gps speed plus or minus speed_error
        speed_error = -123456789
        if not(is_nan(data.fix.eps)):
            speed_error = data.fix.eps
            speed_error = speed_error * 18
            speed_error = speed_error / 5   # converting to km/h
        return speed_error

    def get_utc(self):
        utc = -123456789
        if data.utc != 0 and (not(is_nan(data.utc))):
            utc = data.utc
        return utc

    def get_time(self):
        timestamp = -123456789
        if data.fix.time != 0 and (not(is_nan(data.fix.time))):
            timestamp = data.fix.time
        return timestamp

    def get_heading(self):
        # in degrees.
        # in automotive applications, heading and track are the same
        heading = -123456789
        if data.fix.track != 0 and (not(is_nan(data.fix.track))):
            heading = data.fix.track
        return heading

    def get_heading_error(self):
        # in degrees.
        # 95% chance that true heading is within gps heading plus or minus heading_error
        heading_error = -123456789
        if not(is_nan(data.fix.epd)):
            heading_error = data.fix.epd
        return heading_error



