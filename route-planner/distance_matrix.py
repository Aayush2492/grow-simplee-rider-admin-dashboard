import json
import urllib
import requests
import os

from dotenv import load_dotenv
load_dotenv()


def create_data():
  """Creates the data."""
  data = {}
  data['API_key'] = os.getenv('GOOGLE_MAPS_API_KEY')
  # print(data['API_key'])
  data['addresses'] = []

  # with open("data/drop_points.txt", 'r') as f:
  #   for line in f:
  #       print(line)
  #       line = line.strip().replace(' ', '+')
  #       # line = line.replace(',', '')
  #       data['addresses'].append(line)

  #       if len(data['addresses']) >= 16:
  #         break
    
  data['addresses'] = ['3610+Hacks+Cross+Rd+Memphis+TN', # depot - start point
                       '1921+Elvis+Presley+Blvd+Memphis+TN',
                       '149+Union+Avenue+Memphis+TN',
                       '1034+Audubon+Drive+Memphis+TN',
                       '1532+Madison+Ave+Memphis+TN',
                       '706+Union+Ave+Memphis+TN',
                       '3641+Central+Ave+Memphis+TN',
                       '926+E+McLemore+Ave+Memphis+TN',
                       '4339+Park+Ave+Memphis+TN',
                       '600+Goodwyn+St+Memphis+TN',
                       '2000+North+Pkwy+Memphis+TN',
                       '262+Danny+Thomas+Pl+Memphis+TN',
                       '125+N+Front+St+Memphis+TN',
                       '5959+Park+Ave+Memphis+TN',
                       '814+Scott+St+Memphis+TN',
                       '1005+Tillman+St+Memphis+TN'
                      ]
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]

  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.

  # Maximum number of rows that can be computed per request (6 in this example).
  # print(max_elements)
  # print(num_addresses)
  max_rows = max_elements // num_addresses
  # print(max_rows)

  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []

  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.request.urlopen(request).read()
  response = json.loads(jsonResult)

  # print("Here", response)

  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

def create():
  """Entry point of the program"""
  # Create the data.
  data = create_data()
  distance_matrix = create_distance_matrix(data)

  make_symmetric(distance_matrix)
  # print(distance_matrix)
  return distance_matrix

def make_symmetric(distance_matrix):
  for i in range(len(distance_matrix)):
    for j in range(i, len(distance_matrix)):
      distance_matrix[i][j] = distance_matrix[j][i]

if __name__ == '__main__':
  print(create())