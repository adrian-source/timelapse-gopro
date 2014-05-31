
# author: Adrian Sitterle

# description: 
#               This script will control a gopro camera to take a picture 
#               every day at specified time or times. The script works 
#               by accessing gopro's wifi server commands, that are 
#               executed by making HTTP GET requests with specific parameters.

# script setup:
#               Below, find an array take_picture_on and fill it with as 
#               many hour/minue number pairs as you wish. Make sure they
#               are in 24-hour format.

# hardware setup:
#               Turn on gopro and turn on wifi. Plug in charging cable or
#               a power pack, if you want your timelapse to be longer
#               than 30 minutes.
#               Grab a machine running Python 2 and install python-crontab.
#               Connect the machine to gopro's wifi network and run
#                               sudo python timelapse-gopro.py
#               and leave the machine running for the duration of the 
#               timelapse.

# tested on GoPro Hero 3

# ========= UPDATE VARIABLES BELOW THIS LINE ===============

# Add hour/minute number pairs, of when you want daily picture or 
# pictures to be taken
take_picture_on = [
                # hour, minute
	(17, 00),
	(18, 00)
]

# Update this path with an absolute path to this python file.
# This will be used to generate the cron job.
path = "/Users/adriansitterle/timelapse-gopro.py"

# Replace the X's with your gopro's wifi password
url_pass = "t=XXXXXXXX&"

# ========= UPDATE VARIABLES ABOVE THIS LINE ===============

url_base = "http://10.5.5.9/"

url_gopro_on    = "bacpac/PW?"+url_pass+"p=%01"
url_gopro_off   = "bacpac/PW?"+url_pass+"p=%00"
url_shutter_on  = "bacpac/SH?"+url_pass+"p=%01"
url_shutter_off = "bacpac/SH?"+url_pass+"p=%00"
url_mode_video  = "camera/CM?"+url_pass+"p=%00"
url_mode_photo  = "camera/CM?"+url_pass+"p=%01"
url_fov_wide    = "camera/FV?"+url_pass+"p=%00"
url_fov_med     = "camera/FV?"+url_pass+"p=%01"
url_fov_narrow  = "camera/FV?"+url_pass+"p=%02"
url_vol_no      = "camera/BS?"+url_pass+"p=%00"
url_del_last    = "camera/DL?"+url_pass+"p=%00"
url_led_no      = "camera/LB?"+url_pass+"p=%00"
url_autooff_no  = "camera/AO?"+url_pass+"p=%00"
url_photres_8M  = "camera/PR?"+url_pass+"p=%00"

from crontab import CronTab
import urllib2
from time import sleep
import sys

def new_cron(minute, hour, cmd):

        tab = CronTab(user=True)

        cron_job = tab.new(cmd, comment='from timelapse-gopro.py script')
        cron_job.minute.on(minute)
        cron_job.hour.on(hour)

        if cron_job.is_valid() == False:
                print "problem creating cron job"
                print tab.render()
                exit()

        tab.write()
        print tab.render()


def send_cmd(cmd):
        try:
	print url_base+cmd
                result = urllib2.urlopen(url_base+cmd).read()
                print result
		
        except urllib2.URLError, e:
                print "Error connecting to camera. "
                print e.args

	sleep(1)

def gopro_setup():
        gopro_wake()
        send_cmd(url_vol_no)
        send_cmd(url_led_no)
        send_cmd(url_autooff_no)
        send_cmd(url_photres_8M)
        send_cmd(url_gopro_off)

def gopro_sleep():
        send_cmd(url_gopro_off)

def gopro_wake():
        send_cmd(url_gopro_on)
        sleep(5)  # wait till gopro turns on

def gopro_takepic():
        gopro_wake()
        send_cmd(url_mode_photo)
        sleep(5)  # wait till mode switches
        send_cmd(url_shutter_on)
        sleep(5)  # wait till photo is taken
        gopro_sleep()


if len(sys.argv) == 1:
        print "seting up gopro"
        gopro_setup()
        gopro_sleep()
	
        for entry in take_picture_on:
	print entry
	new_cron(entry[1], entry[0], "python "+path+" takepic")

else:
        print "sending command to gopro "+sys.argv[1]
        if sys.argv[1] == "takepic":
                gopro_takepic()
        elif sys.argv[1] == "sleep":
                gopro_sleep()
        elif sys.argv[1] == "wake":
                gopro_wake()
        elif sys.argv[1] == "setup":
                gopro_setup()


