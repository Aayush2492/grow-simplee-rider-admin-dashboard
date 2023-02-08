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
      <div>
        <Packagecard
          weight={'12 kg'}
          height={'10 cm'}
          breadth={'17 cm'}
          length={'12 cm'}
          expdate={'2023-08-12'}
          exptime={''}
          id={34}
          key={34}
        />
        <br />
      </div>
      <div>
        <Packagecard
          weight={'13 kg'}
          height={'23 cm'}
          breadth={'45 cm'}
          length={'12 cm'}
          expdate={'2023-08-11'}
          exptime={''}
          id={65}
          key={65}
        />
        <br />
      </div>
      {packages.map((item) => {
        return (
          <div>
            <Packagecard
              weight={'23 kg'}
              height={'26 cm'}
              breadth={'35 cm'}
              length={'22 cm'}
              expdate={'2023-08-12'}
              exptime={''}
              id={65}
              key={65}
            />
            <br />
          </div>
        );
      })}
    </div>
  );
}
