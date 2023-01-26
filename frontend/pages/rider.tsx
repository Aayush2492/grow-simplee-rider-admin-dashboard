import React from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { Center } from '@mantine/core';
import RiderNavbar from '../components/RiderNavbar';

const containerStyle = {
  width: '1300px',
  height: '650px',
};

const center = {
  lat: -3.745,
  lng: -38.523,
};

export default function RiderPage({}) {
  // console.log('key', process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY);
  return (
    <RiderNavbar>
      <Center>
        <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY as string}>
          <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={10}></GoogleMap>
        </LoadScript>
      </Center>
    </RiderNavbar>
  );
}
