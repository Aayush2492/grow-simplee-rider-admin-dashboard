import { Card, Group, Text, Badge, Button } from '@mantine/core';

export default function LocationCard() {
  return (
    <div style={{ width: 300 }}>
      <Card shadow="sm" p="lg" radius="md" withBorder>
        <Group position="apart" mt="md" mb="xs">
          <Text weight={500}>Some delivery location</Text>
          <Badge color="red" variant="light">
            Pending
          </Badge>
        </Group>

        <Text size="sm" color="dimmed">
          Address of the delivery location and some extra text some extra text some extra text some
          extra text some extra text
        </Text>

        <Button variant="light" color="blue" fullWidth mt="md" radius="md">
          Show on map
        </Button>
      </Card>
    </div>
  );
}
