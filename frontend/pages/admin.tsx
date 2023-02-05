import React, { useState } from 'react';
import { MapComponent } from '../components/MapComponent';
import { Container, Flex, Drawer } from '@mantine/core';
import AdminNavbar from '../components/Admin/AdminNavbar';

function Admin() {
  const [selectPosition, setSelectPosition] = useState<{ lat: number; lon: number }>({
    lat: 11.9716,
    lon: 77.5946,
  });

  console.log(selectPosition);
  return (
    <>
      <AdminNavbar>
        <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
          <Flex justify="flex-start" align="flex-start" direction="row">
            <Container>
              <MapComponent height={'100vh'} width={'100vw'} selectPosition={selectPosition} />
            </Container>
          </Flex>
        </div>
      </AdminNavbar>
    </>
  );
}

export default Admin;
