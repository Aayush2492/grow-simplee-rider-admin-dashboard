import React from 'react';
import styles from '../css/Box.module.css';
import CardDemo from './CardDemo';
import { IconArrowLeft } from '@tabler/icons';
function Tab3({ addbuttonhandler }) {
  return (
    <div className={styles.tab2}>
      <div className={`${styles.listscrollable}`}>
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
        <br />
        <CardDemo></CardDemo>
      </div>
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
  );
}

export default Tab3;
