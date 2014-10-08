#!/usr/bin/env python
import geoip2.database
from delorean import Delorean

def get_local_time(date, ip):
    reader = geoip2.database.Reader('/Users/scoward/Downloads/GeoIP2-City_20140930/GeoIP2-City.mmdb')
    
    if ip == '127.0.0.1':
        ip = '71.224.243.72'
        # ip = '167.29.0.143'
        # ip = '85.158.202.2'

    response = reader.city(ip)
    local_time_zone = response.location.time_zone

    shifted_date = Delorean(date, 'UTC')
    shifted_date.shift(local_time_zone)
    shifted_date = shifted_date.datetime.strftime('%Y-%m-%d %H:%M:%S')

    return shifted_date