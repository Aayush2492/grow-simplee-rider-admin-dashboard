import { Card, Image, Text, Badge, Button, Group } from '@mantine/core';

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
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ maxWidth: 350, margin: 'auto' }}>
      <Group position="apart" mt="md" mb="xs">
        Object Id : {item.id}
        <Badge color="pink" variant="light">
          Weight : {item.weight}
        </Badge>
        <Badge color="green" variant="light">
          Height : {item.height}
        </Badge>
        <Badge color="orange" variant="light">
          Breadth : {item.breadth}
        </Badge>
        <Badge color="blue" variant="light">
          Length : {item.length}
        </Badge>
      </Group>

      <Text size="sm" color="dimmed">
        Expected Delivery Date :{formatDate(item.expdate)}
      </Text>
      {item.exptime && (
        <Text size="sm" color="dimmed">
          Expected Delivery Time : {item.exptime}
        </Text>
      )}

      <Button variant="light" color="blue" fullWidth mt="md" radius="md">
        Completed
      </Button>
    </Card>
  );
}
