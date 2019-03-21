# Use of Deep Learning to Examine the Association of the Built Environment With Prevalence of Neighborhood Adult Obesity

Data and code repository for the paper available at: https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2698635

The code was written in R and Python 2.7

Users of these code and data should cite *Maharana, A. and Nsoesie, E.O., 2018. Use of deep learning to examine the association of the built environment with prevalence of neighborhood adult obesity. JAMA network open, 1(4), pp.e181535-e181535.* 

Generated figures might differ aesthetically due to post-processing. If you find errors or have questions, please submit an issue.

## Getting Started

This repository contains:
* Census files downloaded from [American Community Survey](https://www.census.gov/programs-surveys/acs)
* Obesity data downloaded from the [500 cities](https://www.cdc.gov/500cities/index.htm) project
* Shapefiles for plotting census tracts of Los Angeles, Memphis, Seattle-Tacoma-Bellevue and San Antonio, downloaded from various sources
* R and Python scripts for preparing data and running the models
* Output files generated from the prediction models

Image feature vector files for each city are too large to be hosted on github. They are available upon request.

Weights for pretrained VGG-CNN-F Caffe model and associated files are available [here](https://gist.github.com/ksimonyan/a32c9063ec8e1118221a#file-readme-md).

### Packages required
R
* MASS
* glmnet
* ggplot2


Python 
* NumPy
* Pandas
* SciPy
* scikit-learn
* Seaborn
* Geospatial Data Abstraction Library (GDAL)
* Caffe ([find instructions here](http://caffe.berkeleyvision.org/installation.html))


## Instructions for downloading satellite images and places of interest data

Requirements
* Obesity prevalence from the 500 cities project
* Shapefiles in the .geojson format
* Google Static Maps API Key

```
cd src
```

### Satellite Images

Make necessary changes to the variables *key*, *city* and *geojsonfile* (required) and other download parameters such as resolution, file format, map type etc. in the script *download_img.py*.
```
python download_img.py
```

### Places of Interest

Make necessary changes to the variables *key*, *city* and *geojsonfile* (required) in the script *download_poi.py*.
```
python download_poi.py
```

## Instructions for preparing feature vectors

### Satellite Image Features using Convolutional Neural Network

Requirements

* VGG_CNN_F Caffe model weights and associated files
* Satellite images

Make necessary changes to the variables *city* and *imgdir* in the script *extract_img_features.py*.
```
python extract_img_features.py
```

Make necessary changes to the variable *city* in the script *img2xy.py*.
```
python img2xy.py
```


### ACS Feature Vector (Socio-economic Factors)

Requirements

* ACS files for each city
* Obesity prevalence from 500 cities project

```
cd src
python aggr_acs.py
```

## Instructions for statistical modeling

Requirements

* Features extracted from the satellite images using CNN
* Points of interest data
* Obesity prevalence from the 500 cities project

To model the association between the features extracted from the satellite images using the CNN and obesity prevalence, the user needs to run

* elasticnet_regression.R

You can use the same script to model the association between the points of interest data and obesity prevalence. The script is located in the src folder. The same script can be used for modeling data for different locations by changing the directory of the data files.


## Instructions for creating figures 

Requirements

* Obesity prevalence from 500 cities project
* File containing model estimated/predicted obesity prevalence 
* Shapefiles 


### Figures 2 and 3 in Main Text

```
cd src
python fig_true_obesity.py
python fig_pred_obesity.py
```

### Part (b) of eFigures 4, 6, 8 and 10 in Supplementary Material 

Uncomment lines 14, 15, and 16 in the script *fig_pred_obesity.py*
```
cd src
python fig_pred_obesity.py
```

### eFigures 15 and 16 in Supplementary Material 

```
cd src
python fig_true_income.py
```
Uncomment lines 18, 19 and 20 in the script *fig_pred_obesity.py*
```
python fig_pred_obesity.py
```

## Acknowledgement
The code used in the script *raycast.py* is from an openly available github repository but.. we forgot to record the project link when we found the code. To whoever is the author of the code, thank you very much for making it available and if you come across this repository, let us know asap. We will add your name and link to your github repository promptly. Thanks!
