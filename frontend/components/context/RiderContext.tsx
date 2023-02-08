import React, { createContext, useState } from 'react';

export const RiderContext = createContext({
  rider: { id: -1, name: '', contact: -1, geoJSON: {} },
  BASE_URL: 'http://127.0.0.1:8000',
  setRider: ({
    id,
    name,
    contact,
    geoJSON,
  }: {
    id: number;
    name: string;
    contact: number;
    geoJSON: {};
  }) => {},
});

const RiderProvider = ({ children }) => {
  const [rider, setRider] = useState<{ id: number; name: string; contact: number; geoJSON: {} }>({
    id: -1,
    name: '',
    contact: -1,
    geoJSON: {},
  });
  const BASE_URL = 'http://127.0.0.1:8000';
  return (
    <RiderContext.Provider value={{ rider, setRider, BASE_URL }}>{children}</RiderContext.Provider>
  );
};

export default RiderProvider;
