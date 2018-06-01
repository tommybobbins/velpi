#!/usr/bin/python
import redis
import subprocess
import logging
from time import sleep
redthis = redis.StrictRedis(host='433host',port=6379, db=0, socket_timeout=3)
#closed_to_half_open.sh
#full_open.sh
#open_to_half_open.sh
#full_close.sh
import logging
FORMAT = "%(asctime)s:%(message)s"
logging.basicConfig(filename='/home/pi/velux_action.txt',level=logging.INFO,format=FORMAT)


def window_task(fromstate,tostate):
        if tostate == "closed":
            logging.info ("We need to run full_close.sh if not already closed")
            if (fromstate == "Closed"):
                logging.info ("We need to do nothing")
            else:
                logging.info ("We need to Close")
                redthis.rpush('attic/jobqueue',"/usr/local/bin/full_close.sh")
#            redthis.set('velux/3','Closed')
        elif tostate == "fullopen":
            logging.info ("We need to run full_open.sh if not already fully open")
#            redthis.set('velux/3','Open')
            if (fromstate == "Open"):
                logging.info ("We need to do nothing")
            else:
                logging.info ("We need to Open")
                redthis.rpush('attic/jobqueue',"/usr/local/bin/full_open.sh")
#            redthis.set('velux/3','Open')
        elif tostate == "halfopen":
            logging.info ("We need to worry about from and to state")
            if (fromstate == "Half"):
                logging.info ("We need to do nothing")
            elif (fromstate == "Closed"):
                redthis.rpush('attic/jobqueue',"/usr/local/bin/closed_to_half_open.sh")
                logging.info ("We need to run closed_to_half_open.sh")
            elif (fromstate == "Open"):
#                redthis.rpush('attic/jobqueue',"/usr/local/bin/open_to_half_open.sh")
                logging.info ("At this point we would have run open_to_half_open.sh")
                logging.info ("But we wont as it will flip flop ")
            elif (fromstate == "ClosedAsleep"):
                logging.info ("We need to run closed_to_half_open.sh")
                redthis.rpush('attic/jobqueue',"/usr/local/bin/closed_to_half_open.sh")
            else:
                redthis.rpush('attic/jobqueue',"/usr/local/bin/closed_to_half_open.sh")
                logging.info ("We need to run closed_to_half_open.sh")
#            redthis.set('velux/3','Half')
        elif tostate == "closedasleep":
            if (fromstate == "ClosedAsleep"):
                logging.info ("We need to do nothing")
            else:
                logging.info ("We need to run all_close.sh and set to closedasleep")
                redthis.rpush('attic/jobqueue',"/usr/local/bin/all_close.sh")
                sleep(60)
                redthis.set('velux/3','ClosedAsleep')
        else: 
            logging.info ("Something has gone wrong")

def study_temperatures(attic,half,full,closed,fromposition):
        if (attic <= closed):
            logging.info ("Attic should be closed")
            window_task(fromposition,"closed")
        elif (attic > closed):
            logging.info ("Ok, so we need to look in more detail") 
            if (attic >= full):
                logging.info ("We should have the window full open")
                window_task(fromposition,"fullopen")
            elif (attic < full):
                logging.info ("We should either have the window half open or closed")
                if (attic < half):
                    if (fromposition == "Closed"):
                        logging.info ("Window is closed and should be")
                        window_task(fromposition,"closed")
                    elif (fromposition == "ClosedAsleep"):
                        logging.info ("Window is closed and should be")
                        window_task(fromposition,"closed")
                    else:
                        logging.info ("Window is not closed ")
                        window_task(fromposition,"halfopen")
                elif (attic >= half):
                    window_task(fromposition,"halfopen")
                else:
                    logging.info ("Something has gone wrong in the attic < half")
            else:
                logging.info ("Something has gone wrong inside the attic >= close clause")
        else:
            logging.info ("Something has gone wrong") 

def check_season(): 
    try:
        holiday = redthis.get("holiday_countdown")
        logging.info("Holiday Countdown exists = %s" % holiday)
    except:
        logging.info("Holiday mode is disabled we need to carry on")
    if  (holiday):
        logging.info("Holiday Countdown exists = %s" % holiday)
        redthis.rpush('attic/jobqueue',"/usr/local/bin/all_close.sh")
        sleep(60)
        exit(0)
    try:
        season = redthis.get("velux/season")
        logging.info("Redis Season velux/season = %s" % season)
    except:
        season = "Winter"
    if (season == "Winter"):
        logging.info("Winter is here, redis down. set velux/season Summer Exiting")
        logging.info("Run the command below to initiate redis")
        logging.info("redis-cli> set velux/season Summer")
        exit(0)
    else:
        logging.info("Summertime. Starting Up")

def control_velux():
    try:
        attic_temp = float(redthis.get('temperature/attic/sensor'))
#        attic_temp = 22.0
        velux_close_trigger = float(redthis.get('temperature/trigger/velux/close'))
        velux_half_open_trigger = float(redthis.get('temperature/trigger/velux/half')) 
        velux_full_open_trigger = float(redthis.get('temperature/trigger/velux/full'))
        velux_state = (redthis.get('velux/3'))
        boiler_been_on = (redthis.get('boiler/4hourtimeout'))
        logging.info ("Attic temp = %f" % attic_temp)
        logging.info ("Half Trigger temp = %f" % velux_half_open_trigger)
        logging.info ("Full Trigger temp = %f" % velux_full_open_trigger)
        logging.info ("Close Trigger temp = %f" % velux_close_trigger)
        logging.info ("Velux state = %s" % velux_state)
        if (boiler_been_on == "True") and (velux_state != "ClosedAsleep") :
            logging.info ("Boiler has been on in the last 4 hours")
            logging.info ("Window not closed asleep Closing")
            window_task(open,"closedasleep")
        elif (boiler_been_on == "True") and (velux_state == "ClosedAsleep"):
            logging.info ("Boiler has been on and window has closed")            
        elif (boiler_been_on != "True"): 
             logging.info ("Boiler has not been on in 4 hours. We can do something \o/ ")            
             study_temperatures(attic_temp, velux_half_open_trigger, velux_full_open_trigger, velux_close_trigger, velux_state)
        else:
             logging.info ("Something has gone wrong")
        sleep(0)
    except:
        logging.info ("Redis down or network unreachable")
        sleep(0)


if __name__ == "__main__":
   check_season()
   while True:
       control_velux() 
       sleep(120)
