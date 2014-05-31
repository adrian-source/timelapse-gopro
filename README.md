timelapse-gopro
===============

 description: 
 
               This script will control a gopro camera to take a picture 
               every day at specified time or times. The script works 
               by accessing gopro's wifi server commands, that are 
               executed by making HTTP GET requests with specific parameters.

 script setup:
 
               Below, find an array take_picture_on and fill it with as 
               many hour/minue number pairs as you wish. Make sure they
               are in 24-hour format.

 hardware setup:
 
               Turn on gopro and turn on wifi. Plug in charging cable or
               a power pack, if you want your timelapse to be longer
               than 30 minutes.
               Grab a machine running Python 2 and install python-crontab.
               Connect the machine to gopro's wifi network and run
               
                               sudo python timelapse-gopro.py
                               
               and leave the machine running for the duration of the 
               timelapse.

 tested on GoPro Hero 3
