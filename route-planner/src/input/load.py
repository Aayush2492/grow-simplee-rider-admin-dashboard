import json
import subprocess

cmd = ['./vroom_binary', '-i','input.json', '-o', 'output.json']
subprocess.run(cmd)

with open('out.json','r') as outfile:
    data = json.load(outfile)
print(type(data))
print(data.keys())

num_tours = data['summary']['routes']

trips = data['routes']
vehicles = []
tours = []

for trip in trips:
    vehicles.append(trip['vehicle'])
    trip_steps = trip['steps']
    curr_tour = []
    curr_tour_index = []
    for i, each_step in enumerate(trip_steps):
        step_type = each_step['type']
        step_loc = each_step['location_index']
        curr_tour.append(step_loc)
        curr_tour_index.append(i)
    tours.append(curr_tour)


print(vehicles)
print('Printing Each Tour')
for trip in tours:
    print(trip)

