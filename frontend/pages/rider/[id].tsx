import React, { useEffect } from 'react';
import { Container, Flex } from '@mantine/core';
import RiderNavbar from '../../components/RiderNavbar';
import { MapComponent } from '../../components/MapComponent';
import { useRouter } from 'next/router';
import { useContext } from 'react';
import { RiderContext } from '../../components/context/RiderContext';

export default function RiderPage() {
  const router = useRouter();
  const { riderId } = router.query;
  const { rider, setRider, BASE_URL } = useContext(RiderContext);

  useEffect(() => {
    console.log(window.location.href);
    const riderIdFromURL = window.location.href.split('/').pop();
    // console.log('riderID', riderIdFromURL);

    const fetchRiderInfo = async () => {
      try {
        const res = await fetch(BASE_URL + '/rider/' + riderIdFromURL);

        if (!res.ok) {
          throw new Error('Error fetching rider data');
        }
        const data = await res.json();

        if (!data) {
          // rider id does not exist in database
          // redirect to 404 page
          router.push('/404');
        }
        console.log('Data', data);
        setRider({ id: data.id, name: data.name, contact: data.contact });
      } catch (err) {
        console.log('Error fetching rider data', err);
      }
    };
    fetchRiderInfo();
  }, []);

  return (
    <>
      <RiderNavbar>
        <div style={{ width: '100vw', height: '100vh', position: 'fixed' }}>
          <Flex justify="flex-start" align="flex-start" direction="row">
            <Container>
              <MapComponent height={'100vh'} width={'100vw'} />
            </Container>
          </Flex>
        </div>
      </RiderNavbar>
    </>
  );
}
