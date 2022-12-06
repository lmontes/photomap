import json
import gpxpy


features = []

with open("data/points.gpx", "r") as file:
    gpx = gpxpy.parse(file)

for (id, wp) in enumerate(gpx.waypoints):
    images = []
    if wp.comment:
        for img in wp.comment.split(","):
            images.append({
                "name": wp.name,
                "url": f"images/{img}",
                "thumbnail": f"thumbnails/{img}"
            })

    feat = {
        "type": "Feature",
        "id": str(id),
        "properties": {
            "name": wp.name,
            "symbol": wp.symbol,
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


geojson = {  
  "type": "FeatureCollection",
  "features": features
}

print(json.dumps(geojson, indent=2))
