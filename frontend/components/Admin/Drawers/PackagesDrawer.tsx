import Packagecard from '../Packagecard';

export default function PackagesDrawer() {
  return (
    <div>
      <Packagecard
        weight={11.5}
        height={12.4}
        breadth={14}
        length={12}
        expdate={'12'}
        exptime={''}
        id={2}
      />
      <br />
      <Packagecard
        weight={11.5}
        height={12.4}
        breadth={14}
        length={12}
        expdate={'12'}
        exptime={''}
        id={2}
      />
      <br />
      <Packagecard
        weight={11.5}
        height={12.4}
        breadth={14}
        length={12}
        expdate={'12'}
        exptime={''}
        id={2}
      />
      <br />
    </div>
  );
}
