import React, { useState } from 'react';
import { Button } from '@mantine/core';
import { Avatar } from '@mantine/core';
import styles from '../css/Box.module.css';
import Tab1 from './Tab1';
import Tab2 from './Tab2';
import Tab3 from './Tab3';

function Box1() {
  const [tab, settab] = useState<Number>(1);
  const addbuttonhandler = (t: Number) => {
    settab(t);
  };
  return (
    <>
      <div className={styles.outerBox1}>
        {tab == 1 ? (
          <Tab1 addbuttonhandler={addbuttonhandler} />
        ) : tab == 2 ? (
          <Tab2 addbuttonhandler={addbuttonhandler} />
        ) : (
          <Tab3 addbuttonhandler={addbuttonhandler} />
        )}
      </div>
      <div className={styles.startbtnup1}>
        <Button variant="white" className={styles.startbtn}>
          START
        </Button>
      </div>
    </>
  );
}

export default Box1;
