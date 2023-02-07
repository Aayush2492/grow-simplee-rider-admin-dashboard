import { useState, useContext, useEffect } from 'react';
import RiderCard from '../RiderCard';
import { PositionContext } from '../../context';

export default function RidersDrawer() {
  const { BASE_URL } = useContext(PositionContext);
  const [riders, setRiders] = useState([]);

  useEffect(() => {
    async function getData() {
      const res = await fetch(`${BASE_URL}/riders`, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await res.json();
      console.log(data);
      setRiders(data);
      console.log(riders);
    }
    getData();
  }, [JSON.stringify(riders)]);

  return (
    <div>
      {riders.map((item) => {
        return (
          <div>
            <RiderCard
              name={item.name}
              contact={item.contact}
              longitude={item.longitude}
              latitude={item.latitude}
              id={item.rider_id}
              key={item.rider_id}
            />
            <br />
          </div>
        );
      })}
    </div>
  );
}
