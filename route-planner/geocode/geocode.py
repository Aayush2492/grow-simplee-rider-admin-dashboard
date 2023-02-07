import pandas as pd
import geocoder # pip install geocoder

# read xlsx
df = pd.read_excel('data/bangalore dispatch address.xlsx')

f = open('lat_long.txt', 'w')

# iterate over rows
for index, row in df.iterrows():
    address = row[0]
    prod_id = row[3]
    edd = row[4]
    g = geocoder.bing(address, key='Ag3_-x9aIPCQxhENQQcDUeFWirDR4tvRr1YUArJF9nrvnUnBv2wis5jue73E_Nxe')
    results = g.json
    f.write(str(prod_id) + ',' + str(edd) + ',' + str(results['lat']) + ',' + str(results['lng']) + '\n')
    # print(results['lat'], results['lng'])
