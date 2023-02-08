import pandas as pd
import geocoder  # pip install geocoder
import random
import time

df = pd.read_excel('data/bangalore_pickups.xlsx')

f = open('final.csv', 'w')

f.write('lat,lng,volume\n')

for index, row in df.iterrows():
    # print(row[0])
    li = []
    for item in row:
        li.append(item)
    address = li[1]
    print(address)
    g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
    results = g.json
    if results is None:
        print('No results found for ' + str(index))
        continue
    random_number = 2 ** random.randint(0, 11 + 1)
    f.write(f'{results["lat"]},{results["lng"]},{random_number*125}\n')

    time.sleep(0.1)
    

f.close()
