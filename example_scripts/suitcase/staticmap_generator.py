import os, json, requests
from dotenv import load_dotenv

# Initialize .env
load_dotenv()

bingmapsAPIKey = os.getenv("bingapiKey")

# Initialize all the HTTP Responses
# getPatterns = f"http://www.ctabustracker.com/bustime/api/v2/getpatterns?key={ctabusapiKey}&format=json&rt=22"
# getVehicles = f"http://www.ctabustracker.com/bustime/api/v2/getvehicles?key={ctabusapiKey}&format=json&rt=22"
# getStops = f"http://www.ctabustracker.com/bustime/api/v2/getstops?key={ctabusapiKey}&format=json&rt=22&dir=Northbound"
# patternResponse = requests.get(getPatterns).json()
# stopsResponse = requests.get(getStops).json()
# vehiclesResponse = requests.get(getVehicles).json()

with open("patterns.json", "r") as a:
    patternResponse = json.load(a)

with open("vehicles.json", "r") as b:
    getVehicles = json.load(b)

with open("stops.json", "r") as c:
    getStops = json.load(c)

bingroutesURL = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes"
stopVar = getStops["bustime-response"]["stops"]
victor = "41.980262,-87.668452"
stpnmofNearest = [
    "Clark & Lawrence",
    "Clark & Ainslie",
    "Clark & Winnemac",
    "Clark & Foster",
    "Clark & Berwyn",
    "Clark & Bryn Mawr",
]
# Example from: https://www.geeksforgeeks.org/python-sort-list-according-to-other-list-order/
# sort_order = ["d", "c", "a", "b"]
# test_list = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]
# res = [tuple for x in sort_order for tuple in test_list if tuple[0] == x]
stopList = [
    (
        stopVar[q]["stpnm"],
        int(stopVar[q]["stpid"]),
        stopVar[q]["lat"],
        stopVar[q]["lon"],
    )
    for q in range(len(stopVar))
]
idofstpsofNrst = [tuple for x in stpnmofNearest for tuple in stopList if tuple[0] == x]
latlotList = [
    ",".join([str(idofstpsofNrst[k][2]), str(idofstpsofNrst[k][3])])
    for k in range(len(idofstpsofNrst))
]
pushpins = "".join(
    "".join([f"pushpin=", latlotList[k], f";46;{k+1}&"]) for k in range(len(latlotList))
)
waypoints = f"waypoint.1={latlotList[0]};57;A&waypoint.2={latlotList[-1]};57;B"
# https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?wp.0=Seattle,WA;64;1&wp.1=Redmond,WA;66;2&key={BingMapsAPIKey}
generatedStaticMap_URL = f"{bingroutesURL}?{waypoints}&{pushpins}key={bingmapsAPIKey}"
