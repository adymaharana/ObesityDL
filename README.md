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
* Caffe  [insert link to download Caffe]



### Instructions for extracting satellite image features


### Instructions for statistical modeling

Needed

* Features extracted from the satellite images using CNN
* Points of interest data
* Obesity prevalence from the 500 cities project

To model the association between the features extracted from the satellite images using the CNN and obesity prevalence, the user needs to run

* elasticnet_regression.R

You can use the same script to model the association between the points of interest data and obesity prevalence. The script is located in the src folder. The same script can be used for modeling data for different locations by changing the directory of the data files.


### Instructions for creating figures 

Needed

* Obesity prevalence from 500 cities project
* File containing model estimated/predicted obesity prevalence 
* Shapefiles 


#### Figures 2 and 3 in Main Text

```
cd src
python fig_pred_obesity.py
```

#### Part (a) of eFigures 4, 6, 8 and 10 in Supplementary Material 

```
cd src
python fig_true_obesity.py
```

#### Figures 2 and 3 in Main Text

```
cd src
python fig_pred_obesity.py
```

#### Part (a) of eFigures 4, 6, 8 and 10 in Supplementary Material 

```
cd src
python fig_true_obesity.py
```

