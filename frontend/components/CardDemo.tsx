import { Card, Image, Text, Badge, Button, Group } from '@mantine/core';

function CardDemo() {
  return (
    <Card shadow="sm" p="lg" radius="md" withBorder style={{ minHeight: 170 }}>
      <Text size="sm" color="dimmed">
        With Fjord Tours you can explore more of the magical fjord landscapes with tours and
        activities on and around the fjords of Norway
      </Text>

      <Button variant="light" color="blue" fullWidth mt="md" radius="md">
        Book classic tour now
      </Button>
    </Card>
  );
}

export default CardDemo;
