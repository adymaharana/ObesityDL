import csv, os, json
import numpy as np


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
    poi_keys.remove('establishment')
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

    return (tract2ind, np.array(poi_feats))

city = 'lacity'
datadir = '../data'

tractids = []
obvalues = {}
with open(os.path.join(datadir, city, '500_cities_' + city + '_obesity.csv'), 'r') as f:
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
print(tractids)

vecdir = '/media/ady/Adyasha1/us_crime'
# outdir = '/media/ady/Adyasha/us_crime/xy'
# vecdir = '/media/ady/Adyasha1/obesity/out'

files = [os.path.join(vecdir, city, f) for f in os.listdir(os.path.join(vecdir, city)) if city in f]
files.sort()
init = False
for file in files:
    if 'filenames' in file:
        if not init:
            filenames = np.load(file)
            init = True
        else:
            temp = np.load(file)
            filenames = np.concatenate((filenames, temp), axis=0)
print(filenames.shape)

init = False
for file in files:
    if 'features' in file:
        if not init:
            features = np.load(file)
            init = True
        else:
            temp = np.load(file)
            features = np.concatenate((features, temp), axis=0)
print(features.shape)

##### clip at 0 (ReLU)
features = np.clip(features, 0, np.amax(features))
##########
count = filenames.shape[0]
start = 0
avgfeatures = []
tractobvals = []
true_pcc = {}
tractids_model = []
for tractid in tractids:
    print(tractid)
    idxs = []
    for i in range(0, count):

        curr_file = str(filenames[i]).split('/')[-1]
        curr_tract = curr_file.split('_')[1]
        if curr_tract == tractid:
            idxs.append(i)
    if idxs == []:
        continue
    avgfeature = np.mean(features[idxs,:], axis=0)
    avgfeatures.append(avgfeature)
    tractobvals.append(float(obvalues[tractid]))
    tractids_model.append(tractid)
# avgpcc = np.array(avgpcc)
avgfeatures = np.array(avgfeatures)
print(avgfeatures.shape)

outdir = '../out'
with open(os.path.join(outdir, city, city + '_tractids_fc7_vggf_z18.txt'), 'w') as f:
    f.write('\n'.join(tractids_model))
#
np.savetxt(os.path.join(outdir, city, 'X_' + city + '_fc7_vggf_z18.txt'), avgfeatures)
np.savetxt(os.path.join(outdir, city, 'y_' + city + '_fc7_vggf_z18.txt'), tractobvals)
