import os,csv

datadir = '../data'
city ='lacity'

def readObfile(obfile):

    tractids = []
    obvalues = {}
    skipped = 0
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
                #print(row)
                skipped += 1
                continue
            tractids.append(row[tractind])
            obvalues[row[tractind]] = float(row[dataind])
    print('Total number of census tracts considered from datafile: ', len(tractids))
    print('Total number of census tracts ignored from datafile (due to population < 50): ', skipped)
    return tractids, obvalues

tractids, _ = readObfile(os.path.join(datadir, city, '500_cities_' + city + '_obesity.csv'))

with open(os.path.join('../out', city, city + '_tractids_fc7_vggf_z18.txt'), 'r') as f:
    tractids_model = f.read().split()

print(len(tractids))
print(len(tractids_model))
print(set(tractids_model)^set(tractids))