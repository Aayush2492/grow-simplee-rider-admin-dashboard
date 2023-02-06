import { Button, TextInput, Center, Textarea, Flex, Autocomplete } from '@mantine/core';
import { DatePicker } from '@mantine/dates';
import { useForm } from '@mantine/form';
import Search from '../Search';
import { useContext, useState } from 'react';
import { PositionContext } from '../../context';

export default function AddNewDeliveryDrawer({ isDelivery }) {
  const form = useForm({
    initialValues: {
      // weight: '',
      // length: '',
      // breadth: '',
      // height: '',
    },

    validate: {
      // email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      // weight: (value: any) => (value > 0 ? null : 'Invalid weight'),
    },
  });

  const { selectPosition, setSelectPosition, BASE_URL } = useContext(PositionContext);

  async function handleSubmit() {
    const latitude = selectPosition.lat;
    const longitude = selectPosition.lon;
    const place = selectPosition.placename;
    console.log('placename', place);

    if (
      !latitude ||
      !longitude ||
      latitude > 90 ||
      latitude < -90 ||
      longitude > 180 ||
      longitude < -180
    ) {
      alert('Please select a valid location: latitude and longitude are not correct');
      return;
    }

    if (!weight || !length || !height || !breadth) {
      alert('Please fill correctly');
      return;
    }

    let response;
    try {
      response = await fetch(`${BASE_URL}/location/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([
          {
            latitude: latitude,
            longitude: longitude,
            // address: values.address,
            address: place,
          },
        ]),
      });

      if (!response.ok) {
        throw new Error('Error in fetch location/');
      }
    } catch (err) {
      alert('error caught in fetch location/');
      console.log(err);
      return;
    }

    const data = await response.json();
    console.log(data);
  }
  const [weight, setweight] = useState('0');
  const [length, setlength] = useState('0');
  const [breadth, setbreadth] = useState('0');
  const [height, setheight] = useState('0');
  return (
    <>
      <form onSubmit={form.onSubmit((values) => handleSubmit())}>
        <br />
        <TextInput
          label="Weight"
          value={weight}
          onChange={(e) => setweight(e.target.value)}
          placeholder="Weight(in kg)"
        />
        <br />
        <Flex justify="flex-start" align="center" direction="row" gap={{ base: 'sm' }}>
          <TextInput
            label="Length"
            placeholder="Length(in cm)"
            value={length}
            onChange={(e) => setlength(e.target.value)}
          />
          <TextInput
            label="Breadth"
            placeholder="Breadth(in cm)"
            value={breadth}
            onChange={(e) => setbreadth(e.target.value)}
          />
          <TextInput
            label="Height"
            placeholder="Height(in cm)"
            value={height}
            onChange={(e) => setheight(e.target.value)}
          />
        </Flex>
        <br />
        <DatePicker
          placeholder="Delivery date"
          label="Event date"
          {...form.getInputProps('date')}
        />
        {/* <TextInput mt="sm" label="Location" placeholder="Location" /> */}
        <br />
        {/* <Search selectPosition={} setSelectPosition={} /> */}
        <Search selectPosition={selectPosition} setSelectPosition={setSelectPosition} />
        <br />
        <Textarea
          placeholder="Your comment"
          label="Your comment"
          withAsterisk
          {...form.getInputProps('comment')}
        />
        <Center>
          <Button type="submit" mt="sm">
            Submit
          </Button>
        </Center>
      </form>
    </>
  );
}
