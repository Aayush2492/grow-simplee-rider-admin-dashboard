# Grow Simplee Backend README
The backend is written in Python with FastAPI framework and Poetry is used for dependency management.
The frontend is written in JavaScript with NextJS framework.
The maps are rendered using `react-leaflet`.

## Instructions to run docker:
There is a `karnataka-latest.osm.pbf` file in the `grow-simplee-rider-admin-dashboard/data_karnataka` folder.

Run the following command to extract some files from the pbf file.

    docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/berlin-latest.osm.pbf || "osrm-extract failed"

Run the following 2 commands

    docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/karnataka-latest.osm.pbf || "osrm-partition failed"
    docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/karnataka-latest.osm.pbf || "osrm-customize failed"

For more information, refer to [this](https://github.com/Project-OSRM/osrm-backend) repo.

## Instructions to build VROOM:
Build VROOM from [this](https://github.com/Project-OSRM/osrm-backend) from the directory `backend/backend/algo`.

## Instructions to run VROOM:
