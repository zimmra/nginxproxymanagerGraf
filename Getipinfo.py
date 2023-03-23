#!/usr/bin/python3

import sys
import geoip2.database
import socket 
import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os

print ('*************************************')
print (sys.argv[1])

print(socket.gethostname())

reader = geoip2.database.Reader('/GeoLite2-City.mmdb')
response = reader.city(str(sys.argv[1]).strip())

Lat = response.location.latitude
ISO = response.country.iso_code
Long = response.location.longitude
State = response.subdivisions.most_specific.name
City = response.city.name
Country = response.country.name
Zip = response.postal.code
IP = str(sys.argv[1]).strip()
Domain = str(sys.argv[2]).strip()
duration = int(sys.argv[3])

reader.close()

# Get environment variables
ifhost = os.getenv('INFLUX_HOST')
ifport = os.getenv('INFLUX_PORT')
ifbucket = os.getenv('INFLUX_BUCKET')
iforg    = os.getenv('INFLUX_ORG')
iftoken  = os.getenv('INFLUX_TOKEN')

print(ifbucket, iforg, ifhost, ifport)

hostname = socket.gethostname()
measurement_name = ("ReverseProxyConnections")
print ('*************************************')
time = datetime.datetime.utcnow()

ifclient = influxdb_client.InfluxDBClient(
    url=f"http://{ifhost}:{ifport}",
    org=iforg,
    token=iftoken
)

write_api = ifclient.write_api(write_options=SYNCHRONOUS)

point = influxdb_client.Point(measurement_name)
point.tag("key", ISO)
point.tag("Latitude", Lat)
point.tag("Longitude", Long)
point.tag("Domain", Domain)
point.tag("City", City)
point.tag("State", State)
point.tag("Name", Country)
point.tag("IP", IP)

point.field("Domain", Domain)
point.field("Latitude", Lat)
point.field("Longitude", Long)
point.field("State", State)
point.field("City", City)
point.field("key", ISO)
point.field("IP", IP)
point.field("Name", Country)
point.field("duration", duration)
point.field("metric", 1)

write_api.write(bucket=ifbucket, org=iforg, record=point)