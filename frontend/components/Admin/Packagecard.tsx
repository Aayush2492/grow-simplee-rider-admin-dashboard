import { Card, Image, Text, Badge, Button, Group, Container } from '@mantine/core';

interface Object {
  id: number;
  weight: number;
  height: number;
  breadth: number;
  length: number;
  expdate: string;
  exptime: string | null;
}

export default function Packagecard(item: Object) {
  const formatDate = (expdate: string) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(expdate).toLocaleDateString('en-IN', options);
  };
  return (
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: '0' }}>
      Object Id : {item.id}
      <Group position="apart" mt="md" mb="xs">
        <Badge color="blue" variant="light">
          Length : {item.length}
        </Badge>
        <Badge color="orange" variant="light">
          Breadth : {item.breadth}
        </Badge>
        <Badge color="green" variant="light">
          Height : {item.height}
        </Badge>
        <Badge color="pink" variant="light">
          Weight : {item.weight}
        </Badge>
      </Group>
      <Text size="sm" style={{ marginTop: '2' }}>
        <b>Expected Delivery Date:</b> {formatDate(item.expdate)}
      </Text>
      {item.exptime && (
        <Text size="sm" color="dimmed">
          Expected Delivery Time : {item.exptime}
        </Text>
      )}
      {item.id % 2 === 0 ? (
        <Button variant="light" color="blue" fullWidth mt="md" radius="md">
          Completed
        </Button>
      ) : (
        <Button variant="light" color="pink" fullWidth mt="md" radius="md">
          Pending
        </Button>
      )}
    </Card>
  );
}
