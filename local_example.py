from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep
import threading
import os
import socket


def udp_receiver(host="10.0.21.238", port=5001):
    # Erstellen Sie ein UDP-Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binden Sie das Socket an eine bestimmte Adresse und Port
    sock.bind((host, port))

    while True:
        # Empfangen Sie Daten vom Client
        data, addr = sock.recvfrom(1024)
        print(f"Empfangene Daten: {data} von {addr}")


class Request:
    def __init__(self, value):
        self.value = value


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")
# time holder for inline commands
ct_g = millis()

# creat simconnection and pass used user classes
sm = SimConnect()
aq = AircraftRequests(sm)
ae = AircraftEvents(sm)

udp_receiver()

sm.createNonATCAircraft(title="Boeing 747-8i Asobo", name="N12345", lat=52.357444, lon=13.519050, rqst=Request(756), hdg=189, gnd=1, alt=160, pitch=0, bank=0, speed=0)
# sleep(0.1)
sm.run_event.wait()
# id = sm.getObjectID()
print(os.environ.get("SIMCONNECT_OBJECT_ID"))
sleep(5)
# sm.set_pos(
#    _Altitude=0,
#    object_id=id,
#    _Latitude=52.357444,
#    _Longitude=13.519050,
#    _Airspeed=0,
#    _Heading=250,
#    _Pitch=0.0,
#    _Bank=0.0,
#    _OnGround=1,
# )
sm.createNonATCAircraft(title="Cessna Skyhawk Asobo", name="N12346", lat=52.357450, lon=13.519055, rqst=Request(10000), hdg=189, gnd=1, alt=160, pitch=0, bank=0, speed=0)
sm.run_event.wait()
print(os.environ.get("SIMCONNECT_OBJECT_ID"))
sleep(2)

# aircraft = sm.getNextDispatch()
# sm.releaseControl(697, Request(182))

# mc = aq.find("MAGNETIC_COMPASS")
# mv = aq.find("MAGVAR")
# print(mc.get() + mv.get())

sleep(300)
sm.exit()
quit()

# Set pos arund space nedle in WA.
sm.set_pos(
    _Altitude=1000.0,
    _Latitude=47.614699,
    _Longitude=-122.358473,
    _Airspeed=130,
    _Heading=250,
    # _Pitch=0.0,
    # _Bank=0.0,
    # _OnGround=0
)

# PARKING_BRAKES = Event(b'PARKING_BRAKES', sm)
# long path
PARKING_BRAKES = ae.Miscellaneous_Systems.PARKING_BRAKES
# using get
GEAR_TOGGLE = ae.Miscellaneous_Systems.get("GEAR_TOGGLE")
# Using find to lookup Event
AP_MASTER = ae.find("AP_MASTER")

# THROTTLE1 Event
THROTTLE1 = ae.Engine.THROTTLE1_SET


# THROTTLE1 Request
Throttle = aq.find("GENERAL_ENG_THROTTLE_LEVER_POSITION:1")

# If useing
# Throttle = aq.find('GENERAL_ENG_THROTTLE_LEVER_POSITION:index')
# Need to set index befor read/write
# Note to set index 2 vs 1 just re-run
# Throttle.setIndex(1)


# print the built in description
# AP_MASTER Toggles AP on/off
print("AP_MASTER", AP_MASTER.description)
# Throttle Percent of max throttle position
print("Throttle", Throttle.description)
# THROTTLE1 Set throttle 1 exactly (0 to 16383)
print("THROTTLE1", THROTTLE1.description)


while not sm.quit:
    print("Throttle:", Throttle.value)
    print("Alt=%f Lat=%f Lon=%f Kohlsman=%.2f" % (aq.PositionandSpeedData.get("PLANE_ALTITUDE"), aq.PositionandSpeedData.get("PLANE_LATITUDE"), aq.PositionandSpeedData.get("PLANE_LONGITUDE"), aq.FlightInstrumentationData.get("KOHLSMAN_SETTING_HG")))
    sleep(2)

    # Send Event with value
    # THROTTLE1(1500)

    # Send Event toggle AP_MASTER
    # AP_MASTER()

    # PARKING_BRAKES()

    # send new data inine @ 5s
    if ct_g + 5000 < millis():
        if Throttle.value < 100:
            Throttle.value += 5
            print("THROTTLE SET")
        ct_g = millis()

sm.exit()
