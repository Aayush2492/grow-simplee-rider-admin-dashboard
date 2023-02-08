docker run -t -v "${PWD}/data_karnataka:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/karnataka-latest.osm.pbf

docker run -t -v "${PWD}/data_karnataka:/data" osrm/osrm-backend osrm-partition /data/karnataka-latest.osrm

docker run -t -v "${PWD}/data_karnataka:/data" osrm/osrm-backend osrm-customize /data/karnataka-latest.osrm

docker run -t -i -p 5000:5000 -v "${PWD}/data:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/karnataka-latest.osrm --max-viaroute-size 15000 --max-trip-size 3000 --max-table-size 3000 --max-matching-size 3000 --max-nearest-size 3000 --max-alternatives 10 --max-matching-radius -1