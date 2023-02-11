import { Card, Text, Badge, Button, Group, List } from '@mantine/core';
import { PositionContext } from '../context';
import { useContext } from 'react';
import { GenjsonContext } from '../context/GeojsonContext';

interface Rider {
  id: number;
  name: string;
  contact: number;
  latitude: number;
  longitude: number;
}

export default function RiderCard(item: Rider) {
  const { geoJSON, setgeoJson } = useContext(GenjsonContext);
  const { selectPosition, setSelectPosition, BASE_URL } = useContext(PositionContext);
  const showGeojson = () => {
    try {
      fetch(BASE_URL + '/rider/' + item.id + '/viewtrip').then((res) =>
        res.json().then((data) => {
          console.log(data['geo-json']);
          setgeoJson(data['geo-json']);
        })
      );
    } catch (err) {
      console.log('Error fetching all locations', err);
    }
  };
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

      <Button variant="light" color="green" fullWidth mt="md" radius="md" onClick={showGeojson}>
        Show route
      </Button>
    </Card>
  );
}
