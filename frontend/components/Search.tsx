import React from 'react';
import Head from 'next/head';
import usePlacesAutocomplete, { getGeocode, getLatLng } from 'use-places-autocomplete';
import useOnclickOutside from 'react-cool-onclickoutside';
import { Input } from '@mantine/core';
import { TextInput, TextInputProps, ActionIcon, useMantineTheme } from '@mantine/core';
import { IconSearch, IconArrowRight, IconArrowLeft } from '@tabler/icons';

function Search() {
  const theme = useMantineTheme();
  const {
    ready,
    value,
    suggestions: { status, data },
    setValue,
    clearSuggestions,
  } = usePlacesAutocomplete({
    requestOptions: {
      /* Define search scope here */
    },
    cache: 24 * 24 * 60,
    debounce: 300,
  });
  const ref = useOnclickOutside(() => {
    // When user clicks outside of the component, we can dismiss
    // the searched suggestions by calling this method
    clearSuggestions();
  });

  const handleInput = (e) => {
    console.log(e.target.value);
    // Update the keyword of the input element
    setValue(e.target.value);
  };

  const handleSelect =
    ({ description }) =>
    () => {
      // When user selects a place, we can replace the keyword without request data from API
      // by setting the second parameter to "false"
      setValue(description, false);
      clearSuggestions();

      // Get latitude and longitude via utility functions
      getGeocode({ address: description }).then((results) => {
        const { lat, lng } = getLatLng(results[0]);
        console.log('📍 Coordinates: ', { lat, lng });
      });
    };

  const renderSuggestions = () =>
    data.map((suggestion) => {
      const {
        place_id,
        structured_formatting: { main_text, secondary_text },
      } = suggestion;

      return (
        <li key={place_id} onClick={handleSelect(suggestion)}>
          <strong>{main_text}</strong> <small>{secondary_text}</small>
        </li>
      );
    });

  return (
    <>
      <div ref={ref}>
        <TextInput
          icon={<IconSearch size={18} stroke={1.5} />}
          radius="xl"
          size="md"
          rightSection={
            <ActionIcon size={32} radius="xl" color={theme.primaryColor} variant="filled">
              {theme.dir === 'ltr' ? (
                <IconArrowRight size={18} stroke={1.5} />
              ) : (
                <IconArrowLeft size={18} stroke={1.5} />
              )}
            </ActionIcon>
          }
          // placeholder="Search questions"
          value={value}
          onChange={handleInput}
          disabled={!ready}
          placeholder="Where are you going?"
          rightSectionWidth={42}
        />
        {/* <input style={{ padding: 10, borderRadius: 2 }} /> */}
        {/* We can use the "status" to decide whether we should display the dropdown or not */}
        {status === 'OK' && (
          <ul style={{ maxHeight: '25vh', overflowY: 'scroll' }}>{renderSuggestions()}</ul>
        )}
      </div>
    </>
  );
}

export default Search;
