import { Title, Text, Anchor, Button } from '@mantine/core';
import useStyles from './Welcome.styles';
import Link from 'next/link'; 

export function Welcome() {
  const { classes } = useStyles();

  return (
    <>
      <Title className={classes.title} align="center" mt={100}>
        Grow Simplee Dashboard
      </Title>
      <Text color="dimmed" align="center" size="lg" sx={{ maxWidth: 580 }} mx="auto" mt="xl">
        Welcome to the dashboard. Choose your role below to get started! <br/>
        <Link href='/admin'>
          <Button fullWidth style={{margin: 20}}> Admin </Button>
        </Link>
        <Link href='/rider'>
          <Button fullWidth style={{margin: 20}}> Rider </Button>
        </Link>
      </Text>
    </>
  );
}
