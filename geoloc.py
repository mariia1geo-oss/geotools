import pandas as pd
from geopy.geocoders import Here
import geopandas
from shapely.geometry import Point

file_in = r'List_of_addresses.csv'

df = pd.read_csv(file_in, sep=';', encoding='UTF8')

df = df.loc[df['formalname_city'] == 'name_city']


df['address_here'] = ""
df['X'] = float(0)
df['Y'] = float(0)

def geo_loc(addr):
    geolocator = Here(app_id='GeolocKey', apikey='apikey')
    location = geolocator.geocode(addr)
    if location:
        return [location.address, location.latitude, location.longitude]
    else:
        return ['', 0, 0]
i=0

def not_na(value):
    if str(value) != 'nan':
        return value
    else:
        empty_val = ''
        return empty_val

for index, row in df.iterrows():
        if str(row['block']) != 'nan':
            block = str(row['block'])
        elif str(row['letter']) != 'nan':
            block = str(row['letter'])
        else:
            block = ''
        if block != '':
            adr = not_na(row['formalname_city']) + ', ' + not_na(row['shortname_street']) + ' ' + not_na(row['formalname_street']) + ', ' + not_na(row['house_number']) + ', ' + block
        else:
            adr = not_na(row['formalname_city']) + ', ' + not_na(row['shortname_street']) + ' ' + not_na(row['formalname_street']) + ', ' + not_na(row['house_number'])
        print(adr)
        try:
            quaters_c = int(row['quarters_count'])
        except:
            quaters_c = 0

        try:
            quaters_l = int(row['living_quarters_count'])
        except:
            quaters_l = 0

        if quaters_c != 0 or quaters_l != 0:
            inf = geo_loc(str(adr))
            print(inf)
            df.loc[index, 'address_here'] = inf[0]
            df.loc[index, 'X'] = inf[2]
            df.loc[index, 'Y'] = inf[1]

df = df.loc[df['address_here'] != '']

geometry = [Point(xy) for xy in zip(df.X, df.Y)]

gdf = geopandas.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)

gdf.to_file(r'point_NN.shp', encoding='UTF-8')