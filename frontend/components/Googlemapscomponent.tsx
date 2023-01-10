import React from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '400px',
  height: '400px',
};

const center = {
  lat: -3.745,
  lng: -38.523,
};

function Googlemapscomponent() {
  return (
    <div>
      <LoadScript googleMapsApiKey="AIzaSyB8wdhAOICu33KIIfInBHJGYZDyDPR6b9w">
        <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={10}>
          {/* Child components, such as markers, info windows, etc. */}
          <></>
        </GoogleMap>
      </LoadScript>
    </div>
  );
}

export default Googlemapscomponent;
