# PiCarWatchman
An IoT Raspberry Pi project to keep tabs on your car.

This IoT device can be installed in your car and will record GPS data, temperature sensors, data from your car's diagnostic system, as well as monitoring your car's battery. The device is powered by your vehicle's own 12V system, and can be configured to run even whilst the vehicle is powered off. Data is transmitted live to a database over 4G LTE cellular networks. 

## System Overview:

![System Overview Diagram](https://github.com/andythomnz/PiCarWatchman/blob/master/images/diagram.png)


A software application will analyse the data transmitted from the vehicle to generate useful analytics.
* Live view showing where the vehicle is on a map and all current sensor values.
* WoF, Service, and Registration reminders
* Finds the start and end data-points for each vehicle journey.
* Summarises statistics for each journey:
   - Trip origin and destination.
   - Plots the journey on a map.
   - Time of departure, time of arrival, trip duration.
   - Distance travelled.
   - Quantity of fuel consumed and cost of trip.
   - Average speed, and how much time was spent idling in traffic.
   
## Discalmer:
*This is an ongoing personal project I began in May 2018, which I have been working on in my spare time.*
I am currently working on assmebling, configuring, and installing the hardware components and the back-end systems which the hardware will upload data to. Once these aspects are in place, I will begin writing a user-oriented front-end application to do useful things with the data gathered.


