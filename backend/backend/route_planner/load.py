import json
import subprocess


def solve_routes(out_file='output.json'):
    """
    Call this function after creating the distance matrix and the input json file
    """
    #direc = 'routing'
    #cmd = [f'./{direc}/vroom_binary', '-i',f'{direc}/input.json', '-o', f'{direc}/{out_file}']
    #subprocess.run(cmd)

    with open(out_file,'r') as outfile:
        data = json.load(outfile)
    print(type(data))
    print(data.keys())

    #num_tours = data['summary']['routes']

    trips = data['routes']
    vehicles = {}
    output = []
    tours = []
    tour_indices = []


    print(vehicles)
    print('Printing Each Tour')
    for rider, objects in trips.items():
        curr_tour = []
        for idx, obj in enumerate(objects):
            #print(obj)
            if obj['type'] != 'job':
                continue
            curr_tour.append(obj['id'])
            output.append([rider, obj['id'], idx])
        # tours.append(curr_tour)
        vehicles[rider] = curr_tour
        

    return  vehicles, output

# vehicles, output = solve_routes()
# print(vehicles, output)
