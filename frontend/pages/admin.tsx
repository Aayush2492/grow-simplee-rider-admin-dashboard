import React, { useState } from 'react';
import Googlemapscomponent from '../components/Googlemapscomponent';
import Box1 from '../components/Box1';
import styles from '../css/Box.module.css';

function Admin() {
  const [display, setdisplay] = useState(true);
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
      <Googlemapscomponent />
      {display ? <Box1 /> : <></>}
      <div className={styles.menuadmin} onClick={() => setdisplay(!display)}>
        <img
          src={display ? '/close.png' : '/menu.png'}
          alt="he"
          style={{ width: 30, height: 30 }}
        />
      </div>
    </div>
  );
}

export default Admin;
