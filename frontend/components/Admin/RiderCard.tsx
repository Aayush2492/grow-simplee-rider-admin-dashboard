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
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: '0' }}>
      <Group position="apart" mt="md" mb="xs">
        <Text>
          <b style={{ color: '#2596be' }}>Rider Name</b>: {item.name}{' '}
        </Text>
        <Text>
          <b style={{ color: '#2596be' }}>Rider Contact</b>: {item.contact}{' '}
        </Text>
        <Badge color="pink" variant="light">
          ID : {item.id}
        </Badge>
      </Group>
      <List>
        <List.Item>
          <b style={{ color: '#2596be' }}>Latitude</b>: {item.latitude}
        </List.Item>
        <List.Item>
          <b style={{ color: '#2596be' }}>Longitude</b>: {item.longitude}
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
        Show current position
      </Button>

      <Button variant="light" color="green" fullWidth mt="md" radius="md">
        Show route
      </Button>
    </Card>
  );
}
