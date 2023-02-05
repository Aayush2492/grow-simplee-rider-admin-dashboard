import { Button, TextInput, Center, Textarea, Flex, Autocomplete } from '@mantine/core';
import { DatePicker } from '@mantine/dates';
import { useForm } from '@mantine/form';
import Search from '../Search';

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

  async function handleSubmit(values: any) {
    console.log(values);

    // const latitude = props.selectPosition.lat;
    // const longitude = props.selectPosition.lon;

    // if (!latitude || !longitude) {
    //   alert('Please select a location: latitude and longitude null');
    //   return;
    // }

    // let response;
    // try {
    //   response = await fetch(`${BASE_URL}/location/`, {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify([
    //       {
    //         latitude: latitude,
    //         longitude: longitude,
    //         // address: values.address,
    //         address: 'OKOKO',
    //       },
    //     ]),
    //   });

    //   if (!response.ok) {
    //     throw new Error('Error in fetch location/');
    //   }
    // } catch (err) {
    //   alert('error caught in fetch location/');
    //   console.log(err);
    //   return;
    // }

    // const data = await response.json();
    // console.log(data);
  }

  return (
    <>
      <form onSubmit={form.onSubmit((values) => handleSubmit(values))}>
        <br />
        <TextInput label="Weight" placeholder="Weight(in kg)" {...form.getInputProps('weight')} />
        <br />
        <Flex justify="flex-start" align="center" direction="row" gap={{ base: 'sm' }}>
          <TextInput label="Length" placeholder="Length(in cm)" {...form.getInputProps('length')} />
          <TextInput
            label="Breadth"
            placeholder="Breadth(in cm)"
            {...form.getInputProps('breadth')}
          />
          <TextInput label="Height" placeholder="Height(in cm)" {...form.getInputProps('height')} />
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
        <Search />
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
