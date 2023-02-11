import React, { createContext, useState } from 'react';

export const GenjsonContext = createContext({
  geoJSON: null,
  setgeoJson: (geoJSON: { type: string; features: [] }) => {},
});

const GeojsonProvider = ({ children }) => {
  const [geoJSON, setgeoJson] = useState<null | { type: string; features: [] }>(null);
  return (
    <GenjsonContext.Provider value={{ geoJSON, setgeoJson }}>{children}</GenjsonContext.Provider>
  );
};

export default GeojsonProvider;
