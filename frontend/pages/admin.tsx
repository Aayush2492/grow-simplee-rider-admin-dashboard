import React, { useContext, useEffect } from 'react';
import { MapComponent } from '../components/MapComponent';
import { Container, Flex, Drawer } from '@mantine/core';
import AdminNavbar from '../components/Admin/AdminNavbar';
import PositionProvider from '../components/context';
import { RiderContext } from '../components/context/RiderContext';
import GeojsonProvider from '../components/context/GeojsonContext';

function Admin() {
  // console.log(selectPosition);
  const { rider, setRider, BASE_URL } = useContext(RiderContext);

  useEffect(() => {
    let sampleGeoJSON = {};
    sampleGeoJSON['type'] = 'FeatureCollection';
    sampleGeoJSON['geometry'] = {
      type: 'Point',
      coordinates: [125.6, 10.1],
    };
    sampleGeoJSON['properties'] = {
      name: 'Dinagat Islands',
    };
    setRider({ ...rider, geoJSON: sampleGeoJSON });
  }, []);

  return (
    <PositionProvider>
      <GeojsonProvider>
        <AdminNavbar>
          <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
            <Flex justify="flex-start" align="flex-start" direction="row">
              <Container>
                <MapComponent height={'100vh'} width={'100vw'} />
              </Container>
            </Flex>
          </div>
        </AdminNavbar>
      </GeojsonProvider>
    </PositionProvider>
  );
}

export default Admin;
