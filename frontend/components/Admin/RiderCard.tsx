import { Card, Text, Badge, Button, Group, List } from '@mantine/core';

interface Rider {
  id: number;
  name: string;
  contact: number;
  latitude: number;
  longitude: number;
}

export default function RiderCard(item: Rider) {
  return (
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: 'auto' }}>
      <Group position="apart" mt="md" mb="xs">
        <Text>Rider Name: {item.name} </Text>
        <Text>Rider Contact: {item.contact} </Text>
        <Badge color="pink" variant="light">
          ID : {item.id}
        </Badge>
      </Group>
      <Text>Current Rider Position</Text>
      <List>
        <List.Item>Latitude: {item.latitude}</List.Item>
        <List.Item>Latitude: {item.longitude}</List.Item>
      </List>
    </Card>
  );
}
