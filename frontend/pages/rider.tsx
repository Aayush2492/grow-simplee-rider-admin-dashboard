import React from 'react';
import { Container, Flex } from '@mantine/core';
import RiderNavbar from '../components/RiderNavbar';
import { MapComponent } from '../components/MapComponent';

export default function RiderPage({}) {
  return (
    <>
      <RiderNavbar>
        <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
          <Flex justify="flex-start" align="flex-start" direction="row">
            <Container>
              <MapComponent height={'100vh'} width={'100vw'} />
            </Container>
          </Flex>
        </div>
      </RiderNavbar>
    </>
  );
}
