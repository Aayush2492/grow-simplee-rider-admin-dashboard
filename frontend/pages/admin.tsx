import React from 'react';
import { MapComponent } from '../components/MapComponent';
import { Container, Flex, Drawer } from '@mantine/core';
import AdminNavbar from '../components/Admin/AdminNavbar';
import PositionProvider from '../components/context';

function Admin() {
  // console.log(selectPosition);
  return (
    <PositionProvider>
      <AdminNavbar>
        <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
          <Flex justify="flex-start" align="flex-start" direction="row">
            <Container>
              <MapComponent height={'100vh'} width={'100vw'} />
            </Container>
          </Flex>
        </div>
      </AdminNavbar>
    </PositionProvider>
  );
}

export default Admin;
