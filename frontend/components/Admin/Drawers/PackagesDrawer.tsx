import { useState, useContext, useEffect } from 'react';
import Packagecard from '../Packagecard';
import { PositionContext } from '../../context';

export default function PackagesDrawer() {
  const { BASE_URL } = useContext(PositionContext);
  const [packages, setPackages] = useState([]);
  console.log(BASE_URL);

  useEffect(() => {
    async function getData() {
      const res = await fetch(`${BASE_URL}/packages`, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await res.json();
      console.log(data);
      setPackages(data);
      console.log(packages);
    }
    getData();
  }, [JSON.stringify(packages)]);

  return (
    <div>
      {packages.map((item) => {
        return (
          <div>
            <Packagecard
              weight={item.weight}
              height={item.height}
              breadth={item.breadth}
              length={item.length}
              expdate={item.delivery_date}
              exptime={''}
              id={item.delivery_loc}
              key={item.delivery_loc}
            />
            <br />
          </div>
        );
      })}
    </div>
  );
}
