import React, { useState } from 'react';
import { TextInput, TextInputProps, ActionIcon, useMantineTheme } from '@mantine/core';
import { IconSearch, IconArrowRight, IconArrowLeft } from '@tabler/icons';
import { Button } from '@mantine/core';

const NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org/search?';
const params = {
  q: '',
  format: 'json',
  addressdetails: 'addressdetails',
};

function Search(props: {
  selectPosition: { lat: number; lon: number };
  setSelectPosition: React.SetStateAction<{ lat: number; lon: number }>;
}) {
  const theme = useMantineTheme();
  const { selectPosition, setSelectPosition } = props;
  const [searchText, setSearchText] = useState('');
  const [listPlace, setListPlace] = useState([]);

  const renderSuggestions = () =>
    listPlace.map((suggestion) => {
      return (
        <li
          key={suggestion?.place_id}
          onClick={() => {
            setSearchText(suggestion.display_name);
            setSelectPosition(suggestion);
            setListPlace([]);
          }}
        >
          <strong style={{ cursor: 'pointer' }}>{suggestion.display_name}</strong>
        </li>
      );
    });

  return (
    <>
      <div>
        <TextInput
          icon={<IconSearch size={18} stroke={1.5} />}
          radius="xl"
          size="md"
          rightSection={
            <ActionIcon size={32} radius="xl" color={theme.primaryColor} variant="filled">
              {theme.dir === 'ltr' ? (
                <IconArrowRight
                  size={18}
                  stroke={1.5}
                  onClick={() => {
                    // Search
                    const params = {
                      q: searchText,
                      format: 'json',
                      addressdetails: 1,
                      polygon_geojson: 0,
                    };
                    const queryString = new URLSearchParams(params).toString();
                    const requestOptions = {
                      method: 'GET',
                      redirect: 'follow',
                    };
                    fetch(`${NOMINATIM_BASE_URL}${queryString}`, requestOptions)
                      .then((response) => response.text())
                      .then((result) => {
                        setListPlace(JSON.parse(result));
                      })
                      .catch((err) => console.log('err: ', err));
                  }}
                />
              ) : (
                <IconArrowLeft
                  size={18}
                  stroke={1.5}
                  onClick={() => {
                    // Search
                    const params = {
                      q: searchText,
                      format: 'json',
                      addressdetails: 1,
                      polygon_geojson: 0,
                    };
                    const queryString = new URLSearchParams(params).toString();
                    const requestOptions = {
                      method: 'GET',
                      redirect: 'follow',
                    };
                    fetch(`${NOMINATIM_BASE_URL}${queryString}`, requestOptions)
                      .then((response) => response.text())
                      .then((result) => {
                        setListPlace(JSON.parse(result));
                      })
                      .catch((err) => console.log('err: ', err));
                  }}
                />
              )}
            </ActionIcon>
          }
          // placeholder="Search questions"
          value={searchText}
          onChange={(e) => {
            setSearchText(e.target.value);
            // Search
            const params = {
              q: searchText,
              format: 'json',
              addressdetails: 1,
              polygon_geojson: 0,
            };
            const queryString = new URLSearchParams(params).toString();
            const requestOptions = {
              method: 'GET',
              redirect: 'follow',
            };
            fetch(`${NOMINATIM_BASE_URL}${queryString}`, requestOptions)
              .then((response) => response.text())
              .then((result) => {
                setListPlace(JSON.parse(result));
              })
              .catch((err) => console.log('err: ', err));
          }}
          // disabled={!ready}
          placeholder="Where are you going?"
          rightSectionWidth={42}
        />
        {/* <input style={{ padding: 10, borderRadius: 2 }} /> */}
        {/* We can use the "status" to decide whether we should display the dropdown or not */}
        {/* {status === 'OK' && (
          <ul style={{ maxHeight: '25vh', overflowY: 'scroll' }}>{renderSuggestions()}</ul>
        )} */}
        {renderSuggestions()}
      </div>
    </>
  );
}

export default Search;
