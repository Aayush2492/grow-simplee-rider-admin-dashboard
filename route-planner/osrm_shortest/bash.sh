#!/bin/bash
endpoint="http://router.project-osrm.org/route/v1/driving/"

#lon,lat coordinates list
waypoints="8.34234,48.23424;8.34423,48.26424;8.36424,48.29424"

format="geojson"

result=$(curl -X GET "${endpoint}/${waypoints}?geometries=${format}")

echo $result > result.json
