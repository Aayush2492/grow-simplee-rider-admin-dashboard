#!/bin/bash
endpoint="http://router.project-osrm.org/route/v1/driving/"

#lon,lat coordinates list
waypoints=$1

format="geojson"

result=$(curl -X GET "${endpoint}/${waypoints}?geometries=${format}")

echo $result > result.json
