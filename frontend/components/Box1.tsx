import React, { useState } from 'react';
import { Button, Modal, TextInput, NumberInput, Center, Textarea } from '@mantine/core';
import { DatePicker } from '@mantine/dates';
import { Avatar } from '@mantine/core';
import styles from '../css/Box.module.css';
import Tab1 from './Tab1';
import Tab2 from './Tab2';
import Tab3 from './Tab3';

function Box1() {
  const [deliveryModalOpened, setDeliveryModalOpened] = useState<Boolean>(false);
  const addbuttonhandler = (flag: Number) => {
    // t == 1 for delivery modal
    // t == 2 for pickup modal
    // t == 3 current rides
    if (flag == 1) setDeliveryModalOpened(true);
    else if (flag == 2) setDeliveryModalOpened(true);
    else if (flag == 3) setDeliveryModalOpened(true);
  };
  return (
    <>
      <Modal
        opened={deliveryModalOpened}
        onClose={() => setDeliveryModalOpened(false)}
        title="Add package details"
      >
        <TextInput label="Weight" placeholder="Weight(in kg)" />
        <TextInput label="Length" placeholder="Length(in cm)" />
        <TextInput label="Breadth" placeholder="Breadth(in cm)" />
        <TextInput label="Height" placeholder="Height(in cm)" />
        <DatePicker placeholder="Delivery date" label="Event date" />
        <TextInput mt="sm" label="Location" placeholder="Location" />
        <Textarea placeholder="Your comment" label="Your comment" withAsterisk />
        <Center>
          <Button type="submit" mt="sm">
            Submit
          </Button>
        </Center>
      </Modal>
      <div className={styles.outerBox1}>
        <Tab1 addbuttonhandler={addbuttonhandler} />
      </div>
      {/* <div className={styles.startbtnup1}>
        <Button variant="white" className={styles.startbtn}>
          START
        </Button>
      </div> */}
    </>
  );
}

export default Box1;
