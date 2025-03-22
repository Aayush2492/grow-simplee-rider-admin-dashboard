import pandas as pd
import geocoder  # pip install geocoder
import random
import time
import csv

f = open('deliveries.csv', 'w')

with open('data/FInal_Evalutation.tsv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    index = 513
    for row in reader:
        address = row[1]
        address = address.lower()
        address += ", bangalore, india"
        print(address)
        g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
        results = g.json
        if results is None:
            print('No results found for ' + str(address))
            # continue
            break
        rand_idx = random.randint(0, 7)
        random_number = 125 * pow(2, rand_idx)
        f.write(f'{index + 1},{results["lat"]},{results["lng"]},{random_number},{row[4]}\n')
        index += 1

f.close()

# for index, row in df.iterrows():
#     li = []
#     for item in row:
#         li.append(item)
#     print(li)
#     address = li[2]
#     address = address.lower()
#     address += ", bangalore, india"
#     print(address)
#     g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
#     results = g.json
#     if results is None:
#         print('No results found for ' + str(index))
#         # continue
#         break
#     random_number = 64000
#     f.write(f'{index + 1},{results["lat"]},{results["lng"]},{random_number},{li[4]}\n')
#     break

#     # time.sleep(0.1)


# f.close()