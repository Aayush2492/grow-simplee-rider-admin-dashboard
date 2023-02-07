# Todos

## Frontend
- complete rider, 
- -complete fetch requests
- admin panel: finish drawers
- check papercuts
- Render GeoJson (this seems to be working, just needs to integrate with fetch)
- Add ID to rider, so that we can simulate differnet riders
- Complete rider panel 

## Backend
- Rider APIS for frontend
- geojson for solveall
- dynamic routing
- check all apis
- solve all with selected packages
- retrieving packages from db, doing a object-index mapping, creating a distance matrix, 
- object model API calls and testing 
- returning geojson testing 
- Simulation for testing? 

## Algo
- We need to test performance with 1000, 2000 points
- Replacing the matrices with np matrices
- Will have to cluster points, based on heuristics like area, date
- Bag pining?
- run vroom on dynamic points hourly
- update distance matrix 
- Testing for last resort:
  - First Cluster by date/area
  - Run vroom separately for every cluster
