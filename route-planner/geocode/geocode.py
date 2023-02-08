import pandas as pd
import geocoder  # pip install geocoder
import random
import time

df = pd.read_excel('data/bangalore dispatch address.xlsx')

f = open('deliveries.csv', 'w')

# with open('data/delivery.csv', 'r') as file:
#     lines = file.readlines()
#     index = 0
#     for line in lines:
#         line = line[:-1]
#         address = line
#         print(address)
#         #  INSERT INTO package (weight, length, breadth, height, delivery_date, delivery_loc, erroneous, comments, obj_type) VALUES (1.0, 1.0, 1.0, 1.0, '2019-01-01 00:00:00', 1, False, 'Dummy', False);
#         g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
#         results = g.json
#         if results is None:
#             print('No results found for ' + str(index))
#             continue

#         # INSERT INTO location(loc_id, latitude, longitude, address) VALUES(12, 12.12, 12.12, 'IITH');
#         f.write(f"INSERT INTO location(loc_id, latitude, longitude, address) VALUES({index}, {results['lat']}, {results['lng']}, 'dummy_{index}');\n")
#         # f.write(f"INSERT INTO package (weight, length, breadth, height, delivery_date, delivery_loc, erroneous, comments, obj_type) VALUES (1.0, 1.0, 1.0, 1.0, '2019-01-01 00:00:00', {index}, False, 'Dummy', False);\n")
#         index += 1

for index, row in df.iterrows():
    li = []
    for item in row:
        li.append(item)
    # print(li)
    address = li[0]
    address = address.lower()
    address += ", bangalore, india"
    print(address)
    g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
    results = g.json
    if results is None:
        print('No results found for ' + str(index))
        continue
    random_number = 64000
    f.write(f'{index + 1},{results["lat"]},{results["lng"]},{random_number},{li[4]}\n')

    # time.sleep(0.1)
    

f.close()
