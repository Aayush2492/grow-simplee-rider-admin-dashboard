coords = []

with open('data/lat_long.csv', 'r') as f:
    lines = f.read().splitlines()
    line = lines[:-1]
    for line in lines:
        lat_long = line.split(',')
        lat = float(lat_long[2])
        long = float(lat_long[3])
        coords.append((lat, long))
        # print(lat, long)

# convert lat, long to geojson point coordinates

with open('data/lat_long.geojson', 'w') as f:
    f.write('{"type": "FeatureCollection", "features": [')
    for coord in coords:
        f.write('{"type": "Feature", "geometry": {"type": "Point", "coordinates": [' + str(coord[1]) + ', ' + str(coord[0]) + ']}, "properties": {"name": "Point"}},')
    f.write(']}')
        