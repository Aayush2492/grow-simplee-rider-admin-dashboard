import React from 'react';
import { MapContainer, Marker, TileLayer, Popup } from 'react-leaflet';

const Map = () => (
  <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '50vh', width: '50vw' }}>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Marker position={[51.505, -0.09]}>
      <Popup>
        A pretty CSS3 popup. <br /> Easily customizable.
      </Popup>
    </Marker>
  </MapContainer>
);

export default Map;
