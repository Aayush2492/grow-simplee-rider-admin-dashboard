import json
import urllib
import requests
import time

from dotenv import load_dotenv
load_dotenv()

def create_data():
  """Creates the data."""
  data = {}
  data['API_key'] = 'Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe'
  # print(data['API_key'])
  data['addresses'] = [] # Stores the lat, longs

  with open("data/lat_long.csv", 'r') as f:
    for line in f:
        # Remove trailing newline
        line = line[:-1]
        elements = line.split(',')
        data['addresses'].append([elements[2], elements[3]])

        if len(data['addresses']) >= 280:
            break

  print("Number of addresses:", len(data['addresses']))
  return data

def create_distance_matrix(data):
  addresses = data["addresses"] # list of lat, longs
  API_key = data["API_key"]
  distance_matrix = [[0] * len(addresses) for i in range(len(addresses))]

  max_elements = 42
  max_elements_2 = 42

  # IMPORTANT: Assuming len(addresses) >= max_elements. Will work on the contrary, but will make more requests.
  for i in range(0, len(addresses), max_elements_2):
    for j in range(i, len(addresses), max_elements):
      print(f"Fetching distance between {i}-{i + max_elements_2 - 1} and {j}-{j + max_elements - 1}")

      origin_addresses = addresses[i: i+max_elements_2]
      dest_addresses = addresses[j:j+max_elements]
      response = send_request(origin_addresses, dest_addresses, API_key)
      temp_distance_matrix = build_distance_matrix(response)
      print("len", len(temp_distance_matrix))

      if len(temp_distance_matrix) == 0:
        print("Error fetching distance matrix")
        print(response)
        exit(1)
      # print(temp_distance_matrix)

      for m in range(len(temp_distance_matrix)):
        for n in range(len(temp_distance_matrix[m])):
          distance_matrix[i + m][j + n] = temp_distance_matrix[m][n]
          distance_matrix[j + n][i + m] = temp_distance_matrix[m][n]

  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):

    request = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?'
    # origins={lat0,long0;lat1,lon1;latM,lonM}&destinations={lat0,lon0;lat1,lon1;latN,longN}&travelMode={travelMode}&startTime={startTime}&timeUnit={timeUnit}&key={BingMapsKey}'
    request += 'travelMode=driving&timeUnit=minute&distanceUnit=km'

    request += '&origins='
    for i in range(len(origin_addresses)):
        request += origin_addresses[i][0] + ',' + origin_addresses[i][1]
        if i == len(origin_addresses) - 1:
            # request += ''
            pass
        else:
            request += ';'

    request += '&destinations='
    for i in range(len(dest_addresses)):
        request += dest_addresses[i][0] + ',' + dest_addresses[i][1]
        if i == len(dest_addresses) - 1:
            # request += '}'
            pass
        else:
            request += ';'

    request += '&key=' + API_key
    # print(request)

    try:
        jsonResult = urllib.request.urlopen(request).read()
    except Exception as e:
        print("Distance Matrix Error:")
        print(e)
        return None
    response = json.loads(jsonResult)

    return response

def build_distance_matrix(response):
    ans = response['resourceSets'][0]['resources'][0]['results']
    distance_matrix = []
    # print(len(ans))
    for i in range(len(ans)):
        distance_matrix.append([])
        distance_matrix[ans[i]['originIndex']].append(ans[i]['travelDistance'])
    return distance_matrix

def create():
  """Entry point of the program"""
  # Create the data.
  data = create_data()

  start = time.time()
  distance_matrix = create_distance_matrix(data)
  end = time.time()
  print("Time taken to create distance matrix:", end - start)

  # make_symmetric(distance_matrix)
  return distance_matrix

if __name__ == '__main__':
  distance_matrix = create()

  with open('data/distance_matrix.txt', 'w') as f:
    for row in distance_matrix:
      f.write(str(row) + '\n')
