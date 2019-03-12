from raycast import *
import urllib.request, urllib.error
import os, json, csv, sys
import numpy as np

maptype = "satellite"
#key = "AIzaSyAUw5RU-RKMK9GgmSI9ZMxGL5ZtKcGgbD0"
key = "AIzaSyDEBmXkpWqV9lZqVvIAXyTjDNN5mJmb7fM"
size = "400x400"
zoom = "18"
fileformat = "png"
city = 'lacity'
datadir = '../data'
outdir = '../out'
# imgdir = '/media/ady/Adyasha1/obesity/lacity_tracts_18_2'
imgdir = '../data/lacity/tract2010'

def getDownloadLocs(boundary_locs):
    p = Polygon([Point(l2, l1) for l1, l2 in boundary_locs])
    lats = [pair[1] for pair in boundary_locs]
    lons = [pair[0] for pair in boundary_locs]
    latMin = min(lats)
    latMax = max(lats)
    lonMin = min(lons)
    lonMax = max(lons)

    download_locs = []
    for i in np.arange(latMin + 0.001, latMax, 0.0013):
        for j in np.arange(lonMin + 0.001, lonMax, 0.0013):
            if p.contains(Point(i, j)):
                download_locs.append((i, j))

    if len(download_locs) == 0:
        download_locs.append(((latMin + latMax) / 2, (lonMin + lonMax) / 2))
    return download_locs

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
                print(row)
                continue
            tractids.append(row[tractind])
            obvalues[row[tractind]] = row[dataind]
    print('Total number of census tracts in datafile: ', len(tractids))
    return tractids, obvalues

def writeLocations(geojsonfile, tractids):

    with open(geojsonfile, 'r') as f:
        shapes = json.load(f)

    print('Number of census tracts in shape file = ' + str(len(shapes['features'])))

    filtered_shapes = []
    count = 0
    for tract in shapes['features']:
        # 'GEOID' for Memphis, Los Angeles (lacity)
        # "TRACT" for San Antonio
        # 'tract2010' for Los Angeles (500 cities)
        # 'STATE' + 'COUNTY' + 'TRACT' for Los Angeles (tiger Shapefile 2010)
        tractid = tract['properties']['STATE'] + tract['properties']['COUNTY'] + tract['properties']['TRACT']
        if tractid not in tractids:
    #         print(tractid)
            continue
        filtered_shapes.append(tract)
    print('Number of census tracts in filtered set: ', len(filtered_shapes))

    locs_by_tract = {}
    # boundary locations are in the counter clockwise direction
    for tract in filtered_shapes:
        print('*', end = ', ')
        sys.stdout.flush()
        boundary_locs = tract['geometry']['coordinates'][0] # for san-antonio
        # boundary_locs = tract['geometry']['coordinates'][0][0] # for lacity
        print(boundary_locs)
    #     print(boundary_locs)
        boundary_locs.reverse()
        tractid = tract['properties']['STATE'] + tract['properties']['COUNTY'] + tract['properties']['TRACT']
        locs = getDownloadLocs(boundary_locs)
        locs_by_tract[tractid] = locs

    f = open(os.path.join(datadir, city, 'download_' + city + '_tract_18_imgs_locs_2.csv'), 'w')
    locwriter = csv.writer(f)
    loc_count = 0
    for tractid in list(locs_by_tract.keys()):
        for i in range(0, len(locs_by_tract[tractid])):
            lat, lon = locs_by_tract[tractid][i]
            loc = str(lat) + ',' + str(lon)
            imgname = city + '_' + tractid + '_' + str(i) + '.png'
            infotext = [imgname, loc, tractid]
            loc_count += 1
            locwriter.writerow(infotext)
    f.close()

    print("Total number of download locations: ", loc_count)
    return

def downloadImages(locfile):

    f = open(locfile, 'r')
    locreader = csv.reader(f)
    download_count = 0
    zoom = '18'
    for row in locreader:

        download_count += 1
        # if download_count <= 18398:
        #     continue
        loc = row[1]
        img_url = "https://maps.googleapis.com/maps/api/staticmap?" + \
                  "center=" + loc + "&" + \
                  "zoom=" + zoom + "&" + \
                  "maptype=" + maptype + "&" + \
                  "size=" + size + "&" + \
                  "format=" + fileformat + "&" + \
                  "key=" + key
        imgname = row[0]
        img_path = os.path.join(imgdir, imgname)
        try:
            urllib.request.urlretrieve(img_url, img_path)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Page not found!")
            elif err.code == 403:
                print("Access denied!")
            else:
                print("Something happened! Error code", err.code)
            print(img_url)
            break
        except urllib.error.URLError as err:
            print("Some other error happened:", err.reason)
            print(img_url)
            break
        print(download_count, end=' ')
        sys.stdout.flush()

    f.close()

if __name__ == "__main__":


    tractids, _ = readObfile(os.path.join(datadir, city, '500_cities_' + city + '_obesity.csv'))

    with open(os.path.join(datadir, city, 'tractids.txt'), 'r') as f:
        tractids_prev = [tract.strip() for tract in f.read().split()]

    tracts_filtered = []
    for tract in tractids:
        if tract in tractids_prev:
            continue
        tracts_filtered.append(tract)
    print(len(tracts_filtered))

    tractids = ['06037930401']

    # geojsonfile = '../data/san-antonio/mapping/Bexar_County_Census_Tracts.geojson'
    # geojsonfile = '../data/lacity/california_census_tracts.geojson'
    # geojsonfile = '../data/lacity/mapping/lacity_census_tracts_2010.geojson'
    geojsonfile = '../data/lacity/tigerShp/gz_2010_06_140_00_500k.json'
    # writeLocations(geojsonfile, tractids)

    locfile = os.path.join(datadir, city, 'download_' + city + '_tract_18_imgs_locs_2.csv')
    downloadImages(locfile)
