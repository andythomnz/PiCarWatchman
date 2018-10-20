import os
import subprocess
import shutil


gps = "unknown"
obd = "unknown"
modem = "unknown"
previousModemDevices = 0
output = subprocess.check_output("dmesg | grep ttyUSB", shell=True)
list = output.splitlines()
for eachLine in list:
    if eachLine.find("pl2303") > -1: #if this is a usb serial device
        usbIndx = eachLine.find("usb")
        port = eachLine[usbIndx+4:usbIndx+11]
        
        if port == "1-1.1.2": #GPS device
            ttyIndx = eachLine.find("ttyUSB")
            gps = eachLine[ttyIndx:]  
        
        if port == "1-1.1.3": #OBD device
            ttyIndex = eachLine.find("ttyUSB")
            obd = eachLine[ttyIndx:]
    elif eachLine.find("GSM modem") > -1: #if this is a modem device
        previousModemDevices = previousModemDevices + 1
        if previousModemDevices == 3:
            ttyIndex = eachLine.find("ttyUSB")
            modem = eachLine[ttyIndex:]

print("GPS is device: " + gps)
print("OBD is device: " + obd)
print("Modem is device: " + modem)

if gps=="unknown" or obd=="unknown" or modem=="unknown":
    print("WARNING: One or more USB devices could not be detected. Expect unpredictable behaviour.")

#Set gpsd configuration to use GPS port
print("Killing all gpsd instances")
try:
    subprocess.check_output("sudo killall gpsd", shell=True)
except subprocess.CalledProcessError:
    print("No gpsd instances running to kill.")

print("Updating gpsd configuration file with correct GPS ttyUSB port..")
gpsdConfigFile = "/etc/default/gpsd"
shutil.move(gpsdConfigFile, gpsdConfigFile+".bak") #backup the existing file

newGpsd = open(gpsdConfigFile, "w")
oldGpsd = open(gpsdConfigFile+".bak", "r")

for eachLine in oldGpsd: #copy contents of old file, but substitude the current GPS port number
    if eachLine.find("ttyUSB") > -1:
        newGpsdLine = "DEVICES=\"/dev/" + gps + "\" \n"
        print("Setting port to: " + "DEVICES=\"/dev/" + gps + "\" \n")
    else:
        newGpsdLine = eachLine
    newGpsd.write(newGpsdLine)
    
newGpsd.close()
oldGpsd.close()

print("Launching gpsd again...")
subprocess.check_output("sudo /etc/init.d/gpsd start", shell=True)

print("Updating data collector configuration with correct OBD ttyUSB port...")
dataCollectorFile = "/home/pi/PiCarWatchman/src/datacollector.py"
shutil.move(dataCollectorFile, dataCollectorFile+".bak") #backup the existing file

newDataCollector = open(dataCollectorFile, "w")
oldDataCollector = open(dataCollectorFile+".bak", "r")

for eachLine in oldDataCollector: #copy contents of old file, but substitude the current OBD port number
    if eachLine.find("ttyUSB") > -1:
        newDataCollectorLine = "obdConnection = obd.OBD(\"/dev/" + obd + "\")\n"
        #newDataCollectorLine = "obdPort = \"/dev/" + obd + "\"\n"
    else:
        newDataCollectorLine = eachLine
    newDataCollector.write(newDataCollectorLine)

newDataCollector.close()
oldDataCollector.close()

#Set wvdial configuration to use modem port
print("Killing all wvdial instances...")
try:
    subprocess.check_output("sudo killall wvdial", shell=True)
except subprocess.CalledProcessError:
    print("No wvdial instances running to kill.")

print("Updating wvdial configuration file with correct modem ttyUSB port..")
wvdialConfigFile = "/etc/wvdial.conf"
shutil.move(wvdialConfigFile, wvdialConfigFile+".bak") #backup the existing file

newConfig = open(wvdialConfigFile, "w")
oldConfig = open(wvdialConfigFile+".bak", "r")

for eachWvdialLine in oldConfig:   #copy contents of old file, but substitude the current modem port number
    if eachWvdialLine.find("/dev") > -1:
        newLine = "Modem = /dev/" + modem + "\n"
        print("Setting port to: " + "Modem = /dev/" + modem + "\n")
    else:
        newLine = eachWvdialLine
    newConfig.write(newLine)

newConfig.close()
oldConfig.close()

print("Launching wvdial again...")
subprocess.check_output("sudo wvdial &> /dev/null", shell=True) #prints wvdial output in python terminal...
#with open(os.devnull, 'wb') as devnull:
#    subprocess.check_call(['sudo /usr/bin/wvdial', ''], stdout=devnull, stderr=subprocess.STDOUT)
