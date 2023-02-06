import React, { createContext, useState } from 'react';

export const PositionContext = createContext({
  selectPosition: { lat: 1000, lon: 1000, placename: '' },
  setSelectPosition: ({
    lat,
    lon,
    placename,
  }: {
    lat: number;
    lon: number;
    placename: string;
  }) => {},
  BASE_URL: 'http://127.0.0.1:8000',
});

const PositionProvider = ({ children }) => {
  const [selectPosition, setSelectPosition] = useState<{
    lat: number;
    lon: number;
    placename: string;
  }>({
    lat: 1000,
    lon: 1000,
    placename: '',
  });
  const BASE_URL = 'http://127.0.0.1:8000';
  return (
    <PositionContext.Provider value={{ selectPosition, setSelectPosition, BASE_URL }}>
      {children}
    </PositionContext.Provider>
  );
};

export default PositionProvider;
