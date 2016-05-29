#!/bin/python

import ConfigParser
import time
import logging
from w1thermsensor import W1ThermSensor

config = ConfigParser.RawConfigParser()
config.read('/etc/logtemp/logtemp.conf')

def clean_get(section, value):
    result = config.get(section, value)
    return result.replace(" ", "_")

logging.basicConfig(filename='/var/log/logtemp.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

t = float(clean_get('log', 'time'))
on = clean_get('log', 'on')

def get_sensor_data():
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            #now = '{:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
            room = clean_get(sensor.id, 'room')
            sensor_name = clean_get(sensor.id, 'name')
            result = room + " " + sensor_name + " " + str(sensor.type_name) + " " + sensor.id + " " + str(sensor.get_temperature(W1ThermSensor.DEGREES_F))
            logging.info(result)

    except Exception, e:
        logging.error('Failed to get sensor information: '+ str(e))

if __name__ == '__main__':
    while on:
        get_sensor_data()
        time.sleep(t)

