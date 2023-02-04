import React, { useState } from 'react';
// import Googlemapscomponent from '../components/Googlemapscomponent';
import Box1 from '../components/Box1';
import styles from '../css/Box.module.css';
import { MapComponent } from '../components/MapComponent';
import { Container, Flex, Button } from '@mantine/core';

function Admin() {
  const [display, setdisplay] = useState(true);
  const [selectPosition, setSelectPosition] = useState<{ lat: number; lon: number }>({
    lat: 12.9716,
    lon: 77.5946,
  });
  return (
    <>
      <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
        <Flex justify="flex-start" align="flex-start" direction="row">
          {display && (
            <Container>
              <Box1 selectPosition={selectPosition} setSelectPosition={setSelectPosition} />
            </Container>
          )}
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
            <MapComponent height={'100vh'} width={'100vw'} selectPosition={selectPosition} />
          </Container>
        </Flex>
      </div>
    </>
  );
}

export default Admin;
