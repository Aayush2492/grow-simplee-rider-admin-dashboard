import json
import urllib
import requests
import os
import time

from dotenv import load_dotenv
load_dotenv()

# def get_place_ids(df):

#   f = open("df/drop_points_place_ids.txt", "w")
#   temp = df['addresses']
#   df['addresses'] = []
#   for index, address in enumerate(temp):
#     print(index + 1)
#     try:
#         address = urllib.parse.quote_plus(address)
#     except Exception as e:
#         print("URL encoding(before calling places API failed) failed")
#         print(e)
    
#     url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
#     url += address
#     url += "&key=" + os.getenv('GOOGLE_MAPS_API_KEY')

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, df=payload)
#     response = json.loads(response.text)

#     if response['status'] != 'OK':
#         print(f"Error fetching place ID for {address}")
#         print(response)
#         print("Exiting...")
#         f.write("ZERO_RESULTS\n")
#         continue
#         # exit(1)

#     if len(response['results']) > 1:
#         print(f"More than one place ID found for {address} ")

#     df['addresses'].append(response['results'][0]['place_id'])
#     f.write(response['results'][0]['place_id'] + "\n")
  
#   f.close()

def create_data():
  """Creates the df."""
  data = {}
  data['API_key'] = os.getenv('GOOGLE_MAPS_API_KEY')
  # print(df['API_key'])
  data['addresses'] = [] # Stores the place ids

  with open("data/drop_points_place_ids.txt", 'r') as f:
    for line in f:
      # Remove trailing newline
      line = line[:-1]

      # TODO: For places with ZERO_RESULTS, no place ID was found by API. Need to deal with this.
      if line != "ZERO_RESULTS":
        data['addresses'].append(line)

      if len(data['addresses']) >= 218:
        break

  # get_place_ids(df)
  # print("print", df['addresses'])
  print("Number of addresses:", len(data['addresses']))
  return data

def create_distance_matrix(data):
  addresses = data["addresses"] # List of place IDs
  API_key = data["API_key"]
  distance_matrix = [[0] * len(addresses) for i in range(len(addresses))]

  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  # and max 25 elements in origin_addresses and 25 in dest_addresses are allowed
  # More info: https://developers.google.com/maps/documentation/distance-matrix/usage-and-billing#other-usage-limits
  max_elements = 25
  max_elements_2 = 4

  # IMPORTANT: Assuming len(addresses) >= max_elements. Will work on the contrary, but will make more requests.
  for i in range(0, len(addresses), max_elements_2):
    for j in range(i, len(addresses), max_elements):
      print(f"Fetching distance between {i}-{i + max_elements_2 - 1} and {j}-{j + max_elements - 1}")
      # print(addresses[i])
      # print(addresses[j:j+max_elements])

      # if i == j:
      #   distance_matrix[i][j] = 0
      #   continue
      
      origin_addresses = addresses[i: i+max_elements_2]
      dest_addresses = addresses[j:j+max_elements]
      response = send_request(origin_addresses, dest_addresses, API_key)
      temp_distance_matrix = build_distance_matrix(response)

      if len(temp_distance_matrix) == 0:
        print("Error fetching distance matrix")
        print(response)
        exit(1)
      # print(temp_distance_matrix)

      for m in range(len(temp_distance_matrix)):
        for n in range(len(temp_distance_matrix[m])):
          distance_matrix[i + m][j + n] = temp_distance_matrix[m][n]
          distance_matrix[j + n][i + m] = temp_distance_matrix[m][n]
      # for k in range(len(temp_distance_matrix[0])):
      #   distance_matrix[i][j + k] = temp_distance_matrix[0][k]
      #   distance_matrix[j + k][i] = temp_distance_matrix[0][k]

  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += "place_id:" + addresses[i] + '|'
    address_str += 'place_id:' + addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key

  try:
    jsonResult = urllib.request.urlopen(request).read()
  except Exception as e:
    print("Distance Matrix Error:")
    print(e)
    return None
  response = json.loads(jsonResult)

  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

def create():
  """Entry point of the program"""
  # Create the df.
  data = create_data()

  start = time.time()
  distance_matrix = create_distance_matrix(data)
  end = time.time()
  print("Time taken to create distance matrix:", end - start)

  # make_symmetric(distance_matrix)
  return distance_matrix

# def make_symmetric(distance_matrix):
#   for i in range(len(distance_matrix)):
#     for j in range(i, len(distance_matrix)):
#       distance_matrix[i][j] = distance_matrix[j][i]

if __name__ == '__main__':
  distance_matrix = create()

  with open('data/distance_matrix.txt', 'w') as f:
    for row in distance_matrix:
      f.write(str(row) + '\n')
  # print(distance_matrix)