import { useState } from 'react';
import {
  Navbar,
  Drawer,
  Tooltip,
  UnstyledButton,
  createStyles,
  Stack,
  Flex,
  Divider,
} from '@mantine/core';
import {
  TablerIcon,
  IconLogout,
  IconTruck,
  IconPackage,
  IconTruckReturn,
  IconBike,
  IconUser,
} from '@tabler/icons';
import AddNewDeliveryDrawer from './Drawers/AddNewDeliveryDrawer';
import styles from '../../css/Box.module.css';
// import AddNewPickUpDrawer from '../Drawers/AddNewPickUpDrawer';
import RidersDrawer from './Drawers/RidersDrawer';
import PackagesDrawer from './Drawers/PackagesDrawer';
import ProfileDrawer from './Drawers/ProfileDrawer';
import { ColorSchemeToggle } from '../ColorSchemeToggle/ColorSchemeToggle';

const useStyles = createStyles((theme) => ({
  link: {
    width: 50,
    height: 50,
    borderRadius: theme.radius.md,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],

    '&:hover': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[0],
    },
  },

  active: {
    '&, &:hover': {
      backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
      color: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color,
    },
  },
}));

interface NavbarLinkProps {
  icon: TablerIcon;
  label: string;
  active?: boolean;
  onClick?(): void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
  const { classes, cx } = useStyles();
  return (
    <Tooltip label={label} position="right" transitionDuration={0}>
      <UnstyledButton onClick={onClick} className={cx(classes.link, { [classes.active]: active })}>
        <Icon stroke={1.5} />
      </UnstyledButton>
    </Tooltip>
  );
}

const mockdata = [
  { icon: IconTruck, label: 'Deliver', title: 'Add New Delivery' },
  { icon: IconTruckReturn, label: 'Pickup', title: 'Add New Pickup Point' },
  { icon: IconBike, label: 'Drivers', title: 'Riders' },
  { icon: IconPackage, label: 'Packages', title: 'Packages' },
  { icon: IconUser, label: 'Profile', title: 'Profile' },
];

export default function AdminNavbar({ children }) {
  const [active, setActive] = useState(0);

  const links = mockdata.map((link, index) => (
    <NavbarLink
      {...link}
      key={link.label}
      active={index === active}
      onClick={() => setActive(index === active ? -1 : index)}
    />
  ));

  return (
    <>
      <Flex
        justify="flex-start"
        align="center"
        direction="row"
        wrap="wrap-reverse"
        gap={{ base: 'sm' }}
      >
        <>
          <Drawer
            opened={active >= 0}
            onClose={() => setActive(-1)}
            title={
              <div style={{ marginLeft: 40, overflow: 'hidden' }}>
                <strong style={{ color: '#2596be' }}>{mockdata[active]?.title}</strong>
                <Divider size="md" />
              </div>
            }
            padding="xl"
            size="xl"
            className={styles.insidediv}
            style={{ translate: '5%' }}
          >
            <div style={{ paddingLeft: 40 }}>
              {active === 0 && <AddNewDeliveryDrawer isDelivery={true} />}
              {active === 1 && <AddNewDeliveryDrawer isDelivery={false} />}
              {active === 2 && <RidersDrawer />}
              {active === 3 && <PackagesDrawer />}
              {active === 4 && <ProfileDrawer />}
            </div>
          </Drawer>
        </>
        <Navbar height={'100vh'} width={{ base: '75px' }} p={'xs'} style={{ overflow: 'hidden' }}>
          <Navbar.Section grow mt={50}>
            <Stack justify="center" spacing={0}>
              {links}
            </Stack>
          </Navbar.Section>
          <Navbar.Section>
            <Stack justify="center" spacing={0}>
              <ColorSchemeToggle />
              <br />
              <NavbarLink icon={IconLogout} label="Logout" />
            </Stack>
          </Navbar.Section>
        </Navbar>
        <>{children}</>
      </Flex>
    </>
  );
}
