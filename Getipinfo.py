#!/usr/bin/python3

import sys
#import geoip2.webservice
print ('*************************************')
print (sys.argv[1])

#print str(sys.argv[1])
import geoip2.database
import socket 

print(socket.gethostname())



reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
response = reader.city(str(sys.argv[1]))

Lat = response.location.latitude
ISO = response.country.iso_code
Long = response.location.longitude
State = response.subdivisions.most_specific.name
City = response.city.name
Country = response.country.name
Zip = response.postal.code
IP = str(sys.argv[1])
Domain = str(sys.argv[2])
duration = int(sys.argv[3])
print (Country)
print (State)
print (City)
print (Zip)
print (Long)
print (Lat)
print (ISO)
print (IP)
reader.close()


import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

## get env vars and use

import os
# influx configuration - edit these

npmhome = "/root/.config/NPMGRAF"
npmhome = os.getenv('NPMGRAF_HOME')
ifuser = os.getenv('INFLUX_USER')
ifpass = os.getenv('INFLUX_PW')
ifdb   = os.getenv('INFLUX_DB')
ifhost = os.getenv('INFLUX_HOST')
ifport = os.getenv('INFLUX_PORT')
ifbucket = os.getenv('INFLUX_BUCKET')
iforg    = os.getenv('INFLUX_ORG')
iftoken  = os.getenv('INFLUX_TOKEN')

hostname = socket.gethostname()
measurement_name = ("ReverseProxyConnections")
print (measurement_name)
print ('*************************************')
# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# format the data as a single measurement for influx
# body = [
#     {
#         "measurement": measurement_name,
#         "time": time,
#         "tags": {
#             "key": ISO,
#             "latitude": Lat,
#             "longitude": Long,
#             "Domain": Domain,
#             "City": City,
#             "State": State,
#             "name": Country,
#             "IP": IP
#             },
#         "fields": {
#             "Domain": Domain,
#             "latitude": Lat,
#             "longitude": Long,
#             "State": State,
#             "City": City,
#             "key": ISO,
#             "IP": IP,
#             "name": Country,
#             "duration": duration,
#             "metric": 1
#         }
#     }
# ]

# connect to influx
# ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
ifclient = influxdb_client.InfluxDBClient(
    url=ifhost,
    org=iforg,
    username=ifuser,
    password=ifpass
)

# write the measurement
write_api = ifclient.write_api(write_options=SYNCHRONOUS)

point = influxdb_client.Point("measurement_name")
point.tag("key", ISO)
point.tag("latitude", Lat)
point.tag("longitude", Long)
point.tag("Domain", Domain)
point.tag("City", City)
point.tag("State", State)
point.tag("name", Country)
point.tag("IP", IP)

point.field("Domain", Domain)
point.field("latitude", Lat)
point.field("longitude", Long)
point.field("State", State)
point.field("City", City)
point.field("key", ISO)
point.field("IP", IP)
point.field("name", Country)
point.field("duration", duration)
point.field("metric", 1)

write_api.write(bucket=ifbucket, org=iforg, record=point)

