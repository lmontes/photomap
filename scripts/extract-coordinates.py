import pathlib
import gpxpy

ID = 1
DATA_DIR = pathlib.Path("data/gpx")

print("lat,lon,type,name,desc,image")


for gpx_filename in DATA_DIR.glob("*.gpx"):
    with open(gpx_filename, "r") as file:
        gpx = gpxpy.parse(file)
    for wp in gpx.waypoints:

        lname = wp.name.lower()
        if "cruce" in lname or "intersección" in lname or "waypoint" in lname:
            continue

        name = wp.name.replace("\n", " ").strip()
        description = ""
        if wp.description and wp.name != wp.description:
            description = wp.description

        print(f"{wp.latitude},{wp.longitude},photo,\"{name}\",\"{description}\",")
