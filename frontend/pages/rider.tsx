import React from 'react';
import { Container, Flex } from '@mantine/core';
import RiderNavbar from '../components/RiderNavbar';
import { MapComponent } from '../components/MapComponent';
import GeojsonProvider from '../components/context/GeojsonContext';

export default function RiderPage() {
  return (
    <GeojsonProvider>
      <>
        <RiderNavbar>
          <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
            <Flex justify="flex-start" align="flex-start" direction="row">
              <Container>
                {/* <MapContainer> */}
                <MapComponent width="100vw" height="100vh" />
                {/* <GeoJSON data={data} /> */}
                {/* </MapContainer> */}
              </Container>
            </Flex>
          </div>
        </RiderNavbar>
      </>
    </GeojsonProvider>
  );
}
