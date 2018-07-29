# PiCarWatchman
An IoT Raspberry Pi project to keep tabs on your car.

This IoT device can be installed in your car and will record GPS data, temperature sensors, data from your car's diagnostic system, as well as monitoring your car's battery. The device is powered by your vehicle's own 12V system, and can be configured to run even whilst the vehicle is powered off. Data is transmitted live to a database over 4G LTE cellular networks. 

A software application will analyse the data transmitted from the vehicle to generate useful analytics.
* Live view showing where the vehicle is on a map and all current sensor values.
* WoF, Service, and Registration reminders
* Finds the start and end data-points for each vehicle journey.
* Summarises statistics for each journey:
..* Trip origin and destination.
..* Plots the journey on a map.
..* Time of departure, time of arrival, trip duration.
..* Distance travelled.
..* Quantity of fuel consumed and cost of trip.
..* Average speed, and how much time was spent idling in traffic.
