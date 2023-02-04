import React, { useState } from 'react';
// import Googlemapscomponent from '../components/Googlemapscomponent';
import Box1 from '../components/Box1';
import styles from '../css/Box.module.css';
import { MapComponent } from '../components/MapComponent';
import { Container, Flex, Button } from '@mantine/core';

function Admin() {
  const [display, setdisplay] = useState(true);
  return (
    <>
      <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
        <Flex justify="flex-start" align="flex-start" direction="row">
          <Container>
            <Box1 />
          </Container>
          <Container>
            <div className={styles.menuadmin} onClick={() => setdisplay(!display)}>
              <img
                src={display ? '/close.png' : '/menu.png'}
                alt="he"
                style={{ width: 30, height: 30 }}
              />
            </div>
            <Button variant="white">START</Button>
          </Container>
          <Container>
            <MapComponent height={'100vh'} width={'66vw'} />
          </Container>
        </Flex>
      </div>
    </>
  );
}

export default Admin;
