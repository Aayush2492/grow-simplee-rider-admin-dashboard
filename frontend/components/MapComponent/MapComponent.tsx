import React from 'react';
import { MapContainer, Marker, TileLayer, Popup, GeoJSON } from 'react-leaflet';

import geoJSONData from '../../data/karnataka_geodata.json';

// const geoJSONData = JSON.parse(

const Map = () => (
  <MapContainer
    center={[12.9716, 77.5946]}
    zoom={10}
    style={{ height: '100vh', width: '66vw' }}
    scrollWheelZoom={false}
  >
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Marker position={[51.505, -0.09]}>
      <Popup>
        A pretty CSS3 popup. <br /> Easily customizable.
      </Popup>
    </Marker>
    {/* GeoJSON data for each route goes here in JSON format. Use OSRM to get LineString output for shortest route between two points */}
    {/* <GeoJSON data={geoJSONData} /> */}
  </MapContainer>
);

export default Map;
