from raycast import *
import urllib.request, urllib.error
import os, json, csv, sys
import numpy as np
import time

key = ""
city = 'lacity'
datadir = '../data'
outdir = '../out'

lat2metres = 110843.73
lon2metres = 96984.22

poi_la = ['establishment', 'bakery', 'real_estate_agency', 'school', 'store', 'car_repair', 'insurance_agency', \
          'restaurant', 'physiotherapist', 'shoe_store', 'lawyer', 'lodging', 'atm', 'general_contractor', \
          'convenience_store', 'electrician', 'beauty_salon', 'art_gallery', 'health', 'bank', 'doctor', 'dentist',
          'neighborhood', 'place_of_worship', 'furniture_store', 'finance', 'gas_station', 'grocery_or_supermarket', \
          'florist', 'home_goods_store', 'car_rental', 'night_club', 'church', 'hair_care', 'fire_station', 'food', \
          'electronics_store', 'moving_company', 'laundry', 'storage', 'plumber', 'car_dealer', 'clothing_store', \
          'pharmacy', 'veterinary_care', 'local_government_office', 'accounting', 'cafe', 'park', 'shopping_mall', \
          'meal_delivery', 'jewelry_store', 'meal_takeaway', 'transit_station', 'spa', 'bus_station', 'premise', 'bar', \
          'movie_theater', 'gym', 'hospital', 'department_store', 'post_office', 'painter', 'travel_agency', 'parking', \
          'airport', 'mosque', 'museum', 'car_wash', 'funeral_home', 'liquor_store', 'embassy', 'library', \
          'roofing_contractor', 'hardware_store', 'book_store', 'courthouse', 'subpremise', 'bicycle_store', 'cemetery', \
          'natural_feature', 'university', 'synagogue', 'city_hall', 'pet_store', 'amusement_park', 'bowling_alley', \
          'stadium', 'movie_rental', 'locksmith', 'taxi_stand', 'campground', 'police', 'light_rail_station', 'rv_park', \
          'aquarium', 'casino', 'train_station', 'zoo', 'hindu_temple']

poi_filt = ['bakery', 'store', 'restaurant', 'physiotherapist', 'lodging', 'atm',  \
          'convenience_store', 'health', 'bank', 'doctor', 'dentist',
          'neighborhood', 'place_of_worship', 'furniture_store', 'finance', 'gas_station', 'grocery_or_supermarket', \
          'florist', 'home_goods_store', 'car_rental', 'night_club', 'church', 'hair_care', 'fire_station', 'food', \
          'electronics_store', 'moving_company', 'laundry', 'storage', 'plumber', 'car_dealer', 'clothing_store', \
          'pharmacy', 'veterinary_care', 'local_government_office', 'accounting', 'cafe', 'park', 'shopping_mall', \
          'meal_delivery', 'jewelry_store', 'meal_takeaway', 'transit_station', 'spa', 'bus_station', 'premise', 'bar', \
          'movie_theater', 'gym', 'hospital', 'department_store', 'post_office', 'painter', 'travel_agency', 'parking', \
          'airport', 'mosque', 'museum', 'car_wash', 'funeral_home', 'liquor_store', 'embassy', 'library', \
          'roofing_contractor', 'hardware_store', 'book_store', 'courthouse', 'subpremise', 'bicycle_store', 'cemetery', \
          'natural_feature', 'university', 'synagogue', 'city_hall', 'pet_store', 'amusement_park', 'bowling_alley', \
          'stadium', 'movie_rental', 'locksmith', 'taxi_stand', 'campground', 'police', 'light_rail_station', 'rv_park', \
          'aquarium', 'casino', 'train_station', 'zoo', 'hindu_temple']

def poi_features(poijsonfile):
    with open(poijsonfile, 'r') as f:
        poi_list = json.load(f)
    print(len(poi_list))

    poi_keys = []
    tract2ind = {}
    for tract, poi_dict in poi_list.items():
        keys = list(poi_dict.keys())
        for key in keys:
            if key not in poi_keys:
                poi_keys.append(key)
    if 'filename' in poi_keys:
        poi_keys.remove('filename')
    if 'loc' in poi_keys:
        poi_keys.remove('loc')
    poi_keys.remove('point_of_interest')
    # poi_keys.remove('establishment')
    poi_keys.remove('locality')
    poi_keys.remove('political')

    print(len(poi_keys))
    print(poi_keys)
    poi_feats = []
    counter = 0
    for tract, poi_dict in poi_list.items():
        tract2ind[tract] = counter
        counter += 1
        temp = [0] * len(poi_keys)
        for i in range(0, len(poi_keys)):
            try:
                temp[i] = poi_dict[poi_keys[i]]
            except KeyError:
                continue
        poi_feats.append(temp)

    return (tract2ind, np.array(poi_feats), poi_keys)

def reorder(poi, order1, order2):
    extras = 0
    counts = []
    for i1 in range(0, len(order1)):
        item1 = order1[i1]
        try:
            i2 = order2.index(item1)
            counts.append(poi[i2])
        except:
            counts.append(0)
            extras += 1
    return counts

def getCentroidParams(boundary_locs):
    # p = Polygon([Point(l2, l1) for l1, l2 in boundary_locs])
    lats = [pair[1] for pair in boundary_locs]
    lons = [pair[0] for pair in boundary_locs]
    latMin = min(lats)
    latMax = max(lats)
    lonMin = min(lons)
    lonMax = max(lons)

    centrLat = (latMin + latMax)/2
    centrLon = (lonMin + lonMax)/2

    radius = int(abs(latMax-latMin)*lat2metres/2) if (abs(latMax-latMin) > abs(lonMax-lonMin)) else int(abs(lonMax-lonMin)*lon2metres/2)

    return centrLat, centrLon, radius

def readObfile(obfile):

    tractids = []
    obvalues = {}
    with open(obfile, 'r') as f:
        obreader = csv.reader(f)
        header = next(obreader)
        for i in range(0, len(header)):
            if header[i] == 'TractFIPS':
                tractind = i
                continue
            if header[i] == 'GeographicLevel':
                levelind = i
                continue
            if header[i] == 'Data_Value':
                dataind = i
                continue
        for row in obreader:
            if row[levelind] != 'Census Tract':
                continue
            if row[dataind] == '':
                # print(row)
                continue
            tractids.append(row[tractind])
            obvalues[row[tractind]] = row[dataind]
    print('Total number of census tracts in datafile: ', len(tractids))
    return tractids, obvalues

def getPOILocations(geojsonfile, tractids):

    with open(geojsonfile, 'r') as f:
        shapes = json.load(f)

    print('Number of census tracts in shape file = ' + str(len(shapes['features'])))

    filtered_shapes = []
    for tract in shapes['features']:
        # 'GEOID' for Memphis
        # "TRACT" for San Antonio
        tractid = tract['properties']["TRACT"]
        if tractid not in tractids:
    #         print(tractid)
            continue
        filtered_shapes.append(tract)
    print('Number of census tracts in filtered set: ', len(filtered_shapes))

    locs_by_tract = {}
    totalLocs = 0
    # boundary locations are in the counter clockwise direction
    for tract in filtered_shapes:
        print('*', end=", ")
        sys.stdout.flush()
        boundary_locs = tract['geometry']['coordinates'][0]
    #     print(boundary_locs)
        boundary_locs.reverse()
        tractid = tract['properties']["TRACT"]
        lat, lon, rad = getCentroidParams(boundary_locs)
        locs_by_tract[tractid] = (lat, lon, rad)
        totalLocs += 1

    print("\nTotal number of download locations: ", totalLocs)
    return locs_by_tract

def downloadPOI(geojsonfile, tractids):

    urlprefix = 'https://maps.googleapis.com/maps/api/place/nearbysearch/'
    output = 'json'

    with open(geojsonfile, 'r') as f:
        shapes = json.load(f)

    print('Number of census tracts in shape file = ' + str(len(shapes['features'])))

    filtered_shapes = []
    for tract in shapes['features']:
        # 'GEOID' for Memphis
        # "TRACT" for San Antonio
        tractid = tract['properties']['GEOID']
        if tractid not in tractids:
    #         print(tractid)
            continue
        filtered_shapes.append(tract)
    print('Number of census tracts in filtered set: ', len(filtered_shapes))

    poi_by_tract = {}
    count = 0
    total = len(filtered_shapes)
    # boundary locations are in the counter clockwise direction
    for tract in filtered_shapes:
        count += 1
        # boundary_locs = tract['geometry']['coordinates'][0] # San Antonio, Memphis
        boundary_locs = tract['geometry']['coordinates'][0][0] # Sea-Tac-Bel
    #     print(boundary_locs)
        boundary_locs.reverse()
        tractid = tract['properties']['GEOID']
        # if tractid != '48029180602':
        #     continue
        lat, lon, radius = getCentroidParams(boundary_locs)
        p = Polygon([Point(l2, l1) for l1, l2 in boundary_locs])

        poi_dict = {}
        url = urlprefix + output + '?location=' + str(lat) + ',' + str(lon) + '&radius=' + str(radius) + '&key=' + key
        jsonfile = 'temp.json'

        addparams = ''
        while True:
            # print(url + addparams)
            try:
                urllib.request.urlretrieve(url + addparams, jsonfile)
            except urllib.error.URLError as err:
                print(tractid, err)
                break

            d = json.load(open(jsonfile, 'r'))
            if d['status'] == "INVALID_REQUEST":
                print('Invalid Request')
                break

            for loc in d['results']:
                poiLat = loc['geometry']['location']['lat']
                poiLon = loc['geometry']['location']['lng']
                if not p.contains(Point(poiLat, poiLon)):
                    continue
                poitypes = loc['types']
                for poi in poitypes:
                    poi_dict.setdefault(poi, 0)
                    poi_dict[poi] += 1

            if 'next_page_token' in d.keys():
                # print('next_page_token= ', d['next_page_token'])
                if d['next_page_token'] != '':
                    addparams = '&pagetoken=' + d['next_page_token']
                    time.sleep(2)
                else:
                    break
            else:
                break

        poi_by_tract[tractid] = poi_dict
        print(count, '/', total, tractid, lat, lon, radius, '*')
        sys.stdout.flush()

    with open(os.path.join(datadir, city, city + '_tract_poi.json'), 'w') as f:
        json.dump(poi_by_tract, f)

    return


def reorder(poi, order1, order2):
    extras = 0
    counts = []
    for i1 in range(0, len(order1)):
        item1 = order1[i1]
        try:
            i2 = order2.index(item1)
            counts.append(int(poi[i2]))
        except:
            counts.append(0)
            extras += 1
    return counts

def poijson2num():

    with open(os.path.join('../out', city, city + '_tractids_fc7_vggf_z18.txt'), 'r') as f:
        tractids_model = f.read().split()
    for i in range(0, len(tractids_model)):
        tractids_model[i] = tractids_model[i].strip('\n')

    tract2index, poifeats, poi_city = poi_features(os.path.join(datadir, city, city + '_tract_poi.json'))

    avgpoi = []
    for tractid in tractids_model:
        poi_ind = tract2index[tractid]
        temp = poifeats[poi_ind]
        poi = reorder(list(temp), poi_la, poi_city)
        avgpoi.append(poi)
    avgpoi = np.array(avgpoi).astype(int)
    print(avgpoi.shape)

    np.savetxt(os.path.join('../out', city, 'X_' + city + '_poi.txt'), avgpoi, fmt='%i')

if __name__ == "__main__":


    tractids, _ = readObfile(os.path.join(datadir, city, '500_cities_' + city + '_obesity.csv'))

    if city == 'san-antonio':
        geojsonfile = '../data/san-antonio/mapping/Bexar_County_Census_Tracts.geojson'
    elif city == 'memphis':
        geojsonfile = '../data/memphis/gisfiles/cb_2016_47_tract_500k.geojson'
    elif city == 'stb':
        geojsonfile = '../data/stb/wa_census_tracts.geojson'
    elif city == 'lacity':
        geojsonfile = '../data/lacity/california_census_tracts.geojson'
    downloadPOI(geojsonfile, tractids)
    poijson2num()