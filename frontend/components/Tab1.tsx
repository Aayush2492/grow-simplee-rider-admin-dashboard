import React from 'react';
import { Button } from '@mantine/core';
import { Avatar } from '@mantine/core';
import styles from '../css/Box.module.css';

function Tab1({ addbuttonhandler }) {
  return (
    <>
      <div className={styles.innerBox1}>
        <div className={styles.avatarbox}>
          <Avatar
            src={require('../public/favicon.svg')}
            alt="it's me"
            sx={{ justifySelf: 'center', margin: 'auto', width: '20px' }}
          />
        </div>
        <div className={styles.naming}>
          <div>Admin Name</div>
          <div>Level 2</div>
        </div>
      </div>
      <div className={styles.buttonsgrp1}>
        <Button
          variant="white"
          fullWidth
          sx={{ color: '#000', fontWeight: 600 }}
          onClick={() => addbuttonhandler(2)}
        >
          Add Delievery Location
        </Button>
        <Button
          variant="white"
          fullWidth
          sx={{ color: '#000', fontWeight: 600 }}
          onClick={() => addbuttonhandler(2)}
        >
          Add Pickup Location
        </Button>
        <Button
          variant="white"
          fullWidth
          sx={{ color: '#000', fontWeight: 600 }}
          onClick={() => addbuttonhandler(3)}
        >
          Show Rides
        </Button>
      </div>
      <Button
        variant="white"
        sx={{
          color: '#000',
          fontWeight: 600,
          maxWidth: '130px',
          textAlign: 'left',
          backgroundColor: '#F7F7F6',
        }}
      >
        Logout &gt;
      </Button>
    </>
  );
}

export default Tab1;
