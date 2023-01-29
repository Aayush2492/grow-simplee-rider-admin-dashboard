import React, { useEffect, useState } from 'react';
import styles from '../css/Box.module.css';
import { IconArrowLeft } from '@tabler/icons';
import Search from './Search';
import Head from 'next/head';
function Tab2({ addbuttonhandler }) {
  const [value, setValue] = useState('');
  return (
    <>
      <Head>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA0tykSlEZB2q8_p5OTPfvFLpWpJuzHfv8&libraries=places"></script>
        s
      </Head>
      <div className={styles.tab2}>
        <div style={{ textAlign: 'center', marginBottom: 15, color: '#000', fontSize: 20 }}>
          Search Location
        </div>
        <Search />
        <div className={styles.backicon}>
          <div
            style={{
              backgroundColor: '#001200',
              padding: 10,
              borderRadius: '50%',
              cursor: 'pointer',
            }}
            onClick={() => addbuttonhandler(1)}
          >
            <IconArrowLeft size={24} stroke={1.5} />
          </div>
        </div>
      </div>
    </>
  );
}

export default Tab2;
