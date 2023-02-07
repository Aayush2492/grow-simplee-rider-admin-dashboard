import { Card, Text, Badge, Button, Group, List } from '@mantine/core';
import { PositionContext } from '../context';
import { useContext } from 'react';

interface Rider {
  id: number;
  name: string;
  contact: number;
  latitude: number;
  longitude: number;
}

export default function RiderCard(item: Rider) {
  const { selectPosition, setSelectPosition, BASE_URL } = useContext(PositionContext);
  return (
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: 'auto' }}>
      <Group position="apart" mt="md" mb="xs">
        <Text>
          <b>Rider Name</b>: {item.name}{' '}
        </Text>
        <Text>
          <b>Rider Contact</b>: {item.contact}{' '}
        </Text>
        <Badge color="pink" variant="light">
          ID : {item.id}
        </Badge>
      </Group>
      <b>Current Rider Position</b>
      <List>
        <List.Item>
          <b>Latitude</b>: {item.latitude}
        </List.Item>
        <List.Item>
          <b>Latitude</b>: {item.longitude}
        </List.Item>
      </List>
      <Button
        variant="light"
        color="blue"
        fullWidth
        mt="md"
        radius="md"
        onClick={() =>
          setSelectPosition({ lat: item.latitude, lon: item.longitude, placename: '' })
        }
      >
        Show on map
      </Button>
    </Card>
  );
}