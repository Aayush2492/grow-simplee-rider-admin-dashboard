sudo docker run -t -v "${PWD}/data:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/southern-zone-latest.osm.pbf

sudo docker run -t -v "${PWD}/data:/data" osrm/osrm-backend osrm-partition /data/southern-zone-latest.osrm

sudo docker run -t -v "${PWD}/data:/data" osrm/osrm-backend osrm-customize /data/southern-zone-latest.osrm

sudo docker run -t -i -p 5000:5000 -v "${PWD}/data:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/southern-zone-latest.osrm --max-viaroute-size 15000 --max-trip-size 3000 --max-table-size 3000 --max-matching-size 3000 --max-nearest-size 3000 --max-alternatives 10 --max-matching-radius -1