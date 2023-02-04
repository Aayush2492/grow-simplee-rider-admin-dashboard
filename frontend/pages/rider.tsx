import React from 'react';
// import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { Center, Container } from '@mantine/core';
import RiderNavbar from '../components/RiderNavbar';
import { MapComponent } from '../components/MapComponent';

export default function RiderPage({}) {
  // console.log('key', process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY);
  return (
    <>
      <RiderNavbar>
        <Container p={0}>
          <MapComponent />
        </Container>
      </RiderNavbar>
    </>
  );
}
