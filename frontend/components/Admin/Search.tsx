import { useState, useRef } from 'react';
import { Autocomplete } from '@mantine/core';

export default function Search({ selectPosition, setSelectPosition }) {
  const NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org/search?';
  const ref = useRef<HTMLInputElement>(null);
  const [data, setData] = useState([]);
  return (
    <>
      <Autocomplete
        label="Location"
        placeholder="Type address here"
        data={data}
        ref={ref}
        onChange={async (newText) => {
          // console.log(newText,data);

          const params = {
            q: newText,
            format: 'json',
            addressdetails: 1,
            polygon_geojson: 0,
          };

          const requestOptions = {
            method: 'GET',
            redirect: 'follow',
          };

          const queryString = new URLSearchParams(params).toString();
          let response;
          try {
            response = await fetch(`${NOMINATIM_BASE_URL}${queryString}`, requestOptions);
            if (!response.ok) {
              throw new Error('Error in autocomplete location search');
            }
          } catch (e) {
            alert('error caught in fetch location/');
            console.error(e);
          }

          const result = await response.text();
          const placesList = JSON.parse(result).map((place) => {
            return {
              value: place.display_name,
              latitude: place.lat,
              longitude: place.lon,
            };
          });
          setData(placesList);
          if (ref.current && ref.current.value && placesList) {
            let p = placesList.filter((x: { value: string }) => x.value == ref.current?.value);
            if (p && p.length) {
              setSelectPosition({
                lat: Number(p[0].latitude),
                lon: Number(p[0].longitude),
                placename: p[0].value,
              });
            }
            // console.log(p);
          }
        }}
      />
    </>
  );
}
