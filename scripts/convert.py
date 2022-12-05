import json
import pathlib
import gpxpy
import numpy as np
import pandas as pd


ID = 1
TOLERANCE = 0.000001
DATA_DIR = pathlib.Path("data/gpx")


df = pd.read_csv("data/metadata.csv")
df[["lat","lon"]] = df[["lat","lon"]].fillna(method="ffill")
df = df.replace([np.nan], [None])


features = []
for gpx_filename in DATA_DIR.glob("*.gpx"):
    with open(gpx_filename, "r") as file:
        gpx = gpxpy.parse(file)
    for wp in gpx.waypoints:

        name = wp.name.lower()
        if "cruce" in name or "intersección" in name or "waypoint" in name:
            continue

        dfm = df[
            (wp.latitude - TOLERANCE <= df["lat"])
            & (df["lat"] <= wp.latitude + TOLERANCE)
            & (wp.longitude - TOLERANCE <= df["lon"])
            & (df["lon"] <= wp.longitude + TOLERANCE)
        ]

        images = []
        for r in dfm.to_dict(orient="records"):
            if r["image"]:
                images.append({
                    "url": f"images/{r['image']}",
                    "thumbnail": f"thumbnails/{r['image']}",
                    "desc": r["desc"]
                })

        feat = {
            "type": "Feature",
            "id": str(ID),
            "properties": {
                "name": wp.name,
                "desc": wp.description if wp.name != wp.description else None,
                "lat": wp.latitude,
                "lon": wp.longitude,
                "images": images
            },
            "geometry": {
                "type": "Point",
                "coordinates": [wp.longitude, wp.latitude]
            }
        }
        features.append(feat)
        ID += 1

geojson = {  
  "type": "FeatureCollection",
  "features": features
}

print(json.dumps(geojson, indent=2))
