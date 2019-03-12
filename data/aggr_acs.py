import os, csv
import numpy as np

datadir = '../data'
city = 'lacity'
# category = ''
# category = '_property'

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


tractids, obvalues = readObfile(os.path.join(datadir, city, '500_cities_' + city + '_obesity.csv'))

# Read file for 2012 5-year ACS estimates of population by census tract
pop_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B01003_with_ann.csv'), 'r') as f:
    popreader = csv.reader(f)
    next(popreader)
    next(popreader)
    for row in popreader:
        tractid = row[1][0:5] + row[1][-6:]
        pop_by_tract[tractid] = int(row[3])
zeroPopTracts = [tid for tid in pop_by_tract.keys() if (pop_by_tract[tid]==0 & (tid in tractids))]
print("Total number of tracts in ACS population estimate file ",  len(pop_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of employment by census tract
empl_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B23025_with_ann.csv'), 'r') as f:
    emplreader = csv.reader(f)
    next(emplreader)
    next(emplreader)
    for row in emplreader:
        tractid = row[1][0:5] + row[1][-6:]
        # print(tractid)
        total = pop_by_tract[tractid]
        empl = int(row[5])
        try:
            percent = float(empl)/total
        except ZeroDivisionError:
            percent = 0.0
        empl_by_tract[tractid] = percent
print("Total number of tracts in ACS employment estimate file ", len(empl_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of poverty by census tract
pov_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B17017_with_ann.csv'), 'r') as f:
    povreader = csv.reader(f)
    next(povreader)
    next(povreader)
    for row in povreader:
        tractid = row[1][0:5] + row[1][-6:]
        total = pop_by_tract[tractid]
        bpl = int(row[5])
        try:
            percent = float(bpl)/total
        except ZeroDivisionError:
            percent = 0
        pov_by_tract[tractid] = percent
print("Total number of tracts in ACS poverty estimate file ", len(pov_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of race by census tract
white_by_tract = {}
black_by_tract = {}
amind_by_tract = {}
asian_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B02001_with_ann.csv'), 'r') as f:
    racereader = csv.reader(f)
    next(racereader)
    next(racereader)
    for row in racereader:
        tractid = row[1][0:5] + row[1][-6:]
        total = int(row[3])
        white = int(row[5])
        black = int(row[7])
        amind = int(row[9])
        asian = int(row[11])
        try:
            percentwh = float(white)/total
            percentbl = float(black)/total
            percentai = float(amind)/total
            percentas = float(asian)/total
        except ZeroDivisionError:
            percentwh = 0
            percentbl = 0
            percentai = 0
            percentas = 0
        white_by_tract[tractid] = percentwh
        black_by_tract[tractid] = percentbl
        amind_by_tract[tractid] = percentai
        asian_by_tract[tractid] = percentas
print("Total number of tracts in ACS race group (white) estimate file ", len(white_by_tract.keys()))
print("Total number of tracts in ACS race group (white) estimate file ", len(black_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of Hispanic population
latino_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B01001I_with_ann.csv'), 'r') as f:
    latreader = csv.reader(f)
    next(latreader)
    next(latreader)
    for row in latreader:
        tractid = row[1][0:5] + row[1][-6:]
        latino = int(row[3])
        try:
            percentlat = float(latino)/pop_by_tract[tractid]
        except (ZeroDivisionError, KeyError) as e:
            percentlat = 0
        latino_by_tract[tractid] = percentlat
print("Total number of tracts in ACS race group (latino) estimate file ", len(latino_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of rent by census tract
rent_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B25064_with_ann.csv'), 'r') as f:
    rentreader = csv.reader(f)
    next(rentreader)
    next(rentreader)
    for row in rentreader:
        tractid = row[1][0:5] + row[1][-6:]
        try:
            rent = int(row[3])
        except ValueError:
            rent = 2000
        rent_by_tract[tractid] = rent
print("Total number of tracts in ACS rent estimate file ", len(rent_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of per capita income by census tract
income_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B19301_with_ann.csv'), 'r') as f:
    increader = csv.reader(f)
    next(increader)
    next(increader)
    for row in increader:
        tractid = row[1][0:5] + row[1][-6:]
        try:
            inc = int(row[3])
        except:
            inc = 0
        income_by_tract[tractid] = inc
print("Total number of tracts in ACS income estimate file ", len(income_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of sex and age groups by census tract
male_by_tract = {}
female_by_tract = {}
age_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B01001_with_ann.csv'), 'r') as f:
    sexreader = csv.reader(f)
    next(sexreader)
    next(sexreader)
    for row in sexreader:
        tractid = row[1][0:5] + row[1][-6:]
        total = pop_by_tract[tractid]
        male = int(row[5])
        female = int(row[53])
        below10idxs = [7, 9, 55, 57]
        below10 = sum([int(row[idx]) for idx in below10idxs])
        _20idxs = [11, 13, 15, 59, 61, 63]
        _20 = sum([int(row[idx]) for idx in _20idxs])
        _30idxs = [17, 19, 21, 23, 65, 67, 69, 71]
        _30 = sum([int(row[idx]) for idx in _30idxs])
        _40idxs = [25, 27, 73, 75]
        _40 = sum([int(row[idx]) for idx in _40idxs])
        _50idxs = [29, 31, 77, 79]
        _50 = sum([int(row[idx]) for idx in _50idxs])
        above50 = total - (below10 + _20 + _30 + _40 + _50)
        if total == 0:
            male_pc = 0
            female_pc = 0
            below10pc = 0
            _20pc = 0
            _30pc = 0
            _40pc = 0
            _50pc = 0
            above50pc = 0
        else:
            male_pc = male/total
            female_pc = female/total
            below10pc = below10/total
            _20pc = _20/total
            _30pc = _30/total
            _40pc = _40/total
            _50pc = _50/total
            above50pc = above50/total
        male_by_tract[tractid] = male_pc
        female_by_tract[tractid] = female_pc
        age_by_tract[tractid] = [below10pc, _20pc, _30pc, _40pc, _50pc, above50pc]
print("Total number of tracts in ACS sex(male) estimate file ", len(male_by_tract.keys()))

# Read file for 2012 5-year ACS estimates of education by census tract
hs_by_tract = {}
clg_by_tract = {}
bach_by_tract = {}
with open(os.path.join(datadir, city, 'ACS_14_5YR_B16010_with_ann.csv'), 'r') as f:
    sexreader = csv.reader(f)
    next(sexreader)
    next(sexreader)
    for row in sexreader:
        tractid = row[1][0:5] + row[1][-6:]
        total = pop_by_tract[tractid]
        hs = int(row[31])
        clg = int(row[57])
        bach = int(row[83])
        if total == 0:
            hs_pc = 0
            clg_pc = 0
            bach_pc = 0
        else:
            hs_pc = hs/total
            clg_pc = clg/total
            bach_pc = bach/total
        hs_by_tract[tractid] = hs_pc
        clg_by_tract[tractid] = clg_pc
        bach_by_tract[tractid] = bach_pc
print("Total number of tracts in ACS education estimate file ", len(hs_by_tract.keys()))

# Read file for census estimates of land area by census tract
area_by_tract = {}
with open(os.path.join(datadir, city, city + '_area.txt'), 'r') as f:
    f.readline()
    for line in f:
        row = line.split()
        area_by_tract[row[1]] = float(row[4])
print("Total number of tracts in area estimate file ", len(area_by_tract.keys()))

# Calculate estimates of population density by census tract
popdens_by_tract = {}
for tractid in pop_by_tract.keys():
    try:
        popdens_by_tract[tractid] = pop_by_tract[tractid]/area_by_tract[tractid]
    except (KeyError, ZeroDivisionError) as e:
        popdens_by_tract[tractid] = 0
print("Total number of tracts in area density estimates ", len(popdens_by_tract.keys()))

print(len(set(empl_by_tract.keys()).intersection(pov_by_tract.keys())))
print(len(set(empl_by_tract.keys()).intersection(white_by_tract.keys())))
print(len(set(empl_by_tract.keys()).intersection(rent_by_tract.keys())))
print(len(set(empl_by_tract.keys()).intersection(income_by_tract.keys())))
print(len(set(pop_by_tract.keys()).intersection(empl_by_tract.keys())))

X = []
y = []
tractids_model = []
vecErr = 0
popErr = 0
crimeKeyErr = 0
popZeroErr = 0
rateErr = 0
print(len(pop_by_tract.keys()))
for tractid in tractids:
    vec = []
    try:
        vec.append(empl_by_tract[tractid])
        vec.append(pov_by_tract[tractid])
        vec.append(white_by_tract[tractid])
        vec.append(rent_by_tract[tractid])
        vec.append(income_by_tract[tractid])
        vec.append(male_by_tract[tractid])
        vec.append(female_by_tract[tractid])
        vec.append(hs_by_tract[tractid])
        vec.append(clg_by_tract[tractid])
        vec.append(popdens_by_tract[tractid])
        # add list of age groups
        vec.extend(age_by_tract[tractid])
        # new additions
        vec.append(bach_by_tract[tractid])
        vec.append(black_by_tract[tractid])
        vec.append(latino_by_tract[tractid])
        vec.append(asian_by_tract[tractid])
        vec.append(amind_by_tract[tractid])

    except:
        vecErr += 1
        continue

    obval = obvalues[tractid]
    tractids_model.append(tractid)
    X.append(vec)
    y.append(obval)

print('#Census Tracts in Model -- #Obesity Values in model -- #KeyError')
print(len(X), len(y), vecErr)
print(max(y))
np.savetxt(os.path.join(datadir, city, 'X_' + city + '_acs.txt'), X)
np.savetxt(os.path.join(datadir, city, 'y_' + city + '_acs.txt'), y)
with open(os.path.join(datadir, city, city + '_tracts_in_acs' + '.txt'), 'w') as f:
    f.write('\n'.join(tractids_model))