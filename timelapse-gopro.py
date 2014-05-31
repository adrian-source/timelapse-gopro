#http://10.5.5.9/bacpac/SH?t=WINDOWS01&p=%00

take_picture_on = [
                # hour, minute
                [9, 0],
                [12, 0],
                [15, 0]
]

url_base = "http://10.5.5.9/"
url_pass = "&t=XXXXXXXXX"

url_gopro_on    = "bacpac/PW?p=%01"
url_gopro_off   = "bacpac/PW?p=%00"
url_shutter_on  = "bacpac/SH?p=%01"
url_shutter_off = "bacpac/SH?p=%00"
url_mode_video  = "camera/CM?p=%00"
url_mode_photo  = "camera/CM?p=%01"
url_fov_wide    = "camera/FV?p=%00"
url_fov_med     = "camera/FV?p=%01"
url_fov_narrow  = "camera/FV?p=%02"
url_vol_no      = "camera/BS?p=%00"
url_del_last    = "camera/DL?p=%00"
url_led_no      = "camera/LB?p=%00"
url_autooff_no  = "camera/AO?p=%00"

from crontab import CronTab
import urllib2
from time import sleep
import sys

def new_cron(minute, hour, cmd):

        tab = CronTab()

        cron_job = tab.new(cmd, comment='from timelapse-gopro.py script')
        cron_job.minute.on(15)
        cron_job.hour.on(minute)

        if cron_job.is_valid() == False:
                print "problem creating cron job"
                print tab.render()
                exit()

        tab.write()
        print tab.render()


def send_cmd(cmd):
        try:
                result = urllib2.urlopen(url_base+cmd+url_pass).read()
                print result
        except urllib2.URLError, e:
                print "Error connecting to camera. "
                print e.args

        sleep(1)

def gopro_setup():
        send_cmd(url_gopro_on)
        send_cmd(url_vol_no)
        send_cmd(url_led_no)
        send_cmd(url_autooff_no)

        send_cmd(url_mode_photo)
        send_cmd(url_fov_narrow)

def gopro_takepic():
        send_cmd(url_shutter_on)

def gopro_sleep():
        send_cmd(url_gopro_off)

def gopro_wake():
        send_cmd(url_gopro_on)


if len(sys.argv) == 1:
        print "seting up gopro"
        gopro_setup()
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

