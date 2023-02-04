import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { MapContainer, Marker, TileLayer, Popup, GeoJSON, useMap } from 'react-leaflet';

import geoJSONData from '../../data/karnataka_geodata.json';

const icon = L.icon({
  iconUrl: require('../../public/map.png'),
  iconSize: [38, 38],
});

// const geoJSONData = JSON.parse(
function ResetCenterView(props: { selectPosition: null | { lat: number; lon: number } }) {
  const { selectPosition } = props;
  const map = useMap();

  useEffect(() => {
    if (selectPosition) {
      map.setView(L.latLng(selectPosition?.lat, selectPosition?.lon), map.getZoom(), {
        animate: true,
      });
    }
  }, [selectPosition]);

  return null;
}

export default function Map({
  height,
  width,
  selectPosition,
}: {
  height: string;
  width: string;
  selectPosition: null | { lat: number; lon: number };
}) {
  const locationSelection = [selectPosition?.lat, selectPosition?.lon];
  return (
    <MapContainer
      center={[12.9716, 77.5946]}
      zoom={10}
      style={{ height: height, width: width, position: 'fixed', top: 0, left: 0, zIndex: 0 }}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {selectPosition && (
        <Marker position={locationSelection} icon={icon}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      )}
      <ResetCenterView selectPosition={selectPosition} />
      {/* GeoJSON data for each route goes here in JSON format. Use OSRM to get LineString output for shortest route between two points */}
      {/* <GeoJSON data={geoJSONData} /> */}
    </MapContainer>
  );
}
