import React, { useContext, useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MapContainer, Marker, TileLayer, Popup, GeoJSON, useMap } from 'react-leaflet';

// import geoJSONData from '../../data/karnataka_geodata.json';
import { PositionContext } from '../context';
import { RiderContext } from '../context/RiderContext';

const icon = L.icon({
  iconUrl: 'map.png',
  iconSize: [38, 38],
});

// const geoJSONData = JSON.parse(
function ResetCenterView(props: { selectPosition: null | { lat: number; lon: number } }) {
  const { selectPosition } = props;
  const map = useMap();

  useEffect(() => {
    if (
      selectPosition &&
      selectPosition.lat <= 90 &&
      selectPosition.lat >= -90 &&
      selectPosition.lon <= 180 &&
      selectPosition.lon >= -180
    ) {
      map.setView(L.latLng(selectPosition?.lat, selectPosition?.lon), map.getZoom(), {
        animate: true,
      });
    }
  }, [selectPosition]);

  return null;
}

export default function Map({ height, width }: { height: string; width: string }) {
  const { rider, setRider, BASE_URL } = useContext(RiderContext);

  console.log('Rider', rider);
  // console.log('geo', geoJSONData);
  // const [locationSelection, setlocationSelection] = useState([
  //   selectPosition.lat <= 90 && selectPosition.lat >= -90 ? selectPosition.lat : 12.9716,
  //   selectPosition.lon <= 180 && selectPosition.lon >= -180 ? selectPosition.lon : 77.5946,
  // ]);

  // useEffect(() => {
  //   setlocationSelection([
  //     selectPosition.lat <= 90 && selectPosition.lat >= -90 ? selectPosition.lat : 12.9716,
  //     selectPosition.lon <= 180 && selectPosition.lon >= -180 ? selectPosition.lon : 77.5946,
  //   ]);
  // }, []);

  const { selectPosition } = useContext(PositionContext);

  return (
    <MapContainer
      center={[
        selectPosition.lat <= 90 && selectPosition.lat >= -90 ? selectPosition.lat : 12.9716,
        selectPosition.lon <= 180 && selectPosition.lon >= -180 ? selectPosition.lon : 77.5946,
      ]}
      zoom={10}
      style={{ height: height, width: width, position: 'fixed', top: 0, left: 0, zIndex: 0 }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {selectPosition && (
        <Marker
          position={[
            selectPosition.lat <= 90 && selectPosition.lat >= -90 ? selectPosition.lat : 12.9716,
            selectPosition.lon <= 180 && selectPosition.lon >= -180 ? selectPosition.lon : 77.5946,
          ]}
          icon={icon}
        >
          <Popup>
            Latitude : {selectPosition.lat} <br /> Longitude : {selectPosition.lon}
          </Popup>
        </Marker>
      )}
      <ResetCenterView selectPosition={selectPosition} />
      {/* GeoJSON data for each route goes here in JSON format. Use OSRM to get LineString output for shortest route between two points */}
      {/* <GeoJSON data={{}} /> */}
    </MapContainer>
  );
}
