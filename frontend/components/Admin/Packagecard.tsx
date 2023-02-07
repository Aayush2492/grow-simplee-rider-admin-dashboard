import { Card, Image, Text, Badge, Button, Group } from '@mantine/core';

export default function Packagecard({ id, weight, height, breadth, length, expdate, exptime }) {
  return (
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: 'auto' }}>
      <Group position="apart" mt="md" mb="xs">
        Object Id : {id}
        <Badge color="pink" variant="light">
          Weight : {weight}
        </Badge>
        <Badge color="green" variant="light">
          Height : {height}
        </Badge>
        <Badge color="orange" variant="light">
          Breadth : {breadth}
        </Badge>
        <Badge color="blue" variant="light">
          Length : {length}
        </Badge>
      </Group>

      <Text size="sm" color="dimmed">
        Expected Delivery Date :{expdate}
      </Text>
      {exptime && (
        <Text size="sm" color="dimmed">
          Expected Delivery Time : {exptime}
        </Text>
      )}

      <Button variant="light" color="blue" fullWidth mt="md" radius="md">
        Completed
      </Button>
    </Card>
  );
}
