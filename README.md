# Use of Deep Learning to Examine the Association of the Built Environment With Prevalence of Neighborhood Adult Obesity

Data and code repository for the paper available at: https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2698635

The code was written in R and Python 2.7

Users of these code and data should cite Maharana, A. and Nsoesie, E.O., 2018. Use of deep learning to examine the association of the built environment with prevalence of neighborhood adult obesity. JAMA network open, 1(4), pp.e181535-e181535. 

Generated figures might differ aesthetically due to post-processing. If you find errors or have questions, please submit an issue.

## Getting Started

This repository contains:
* Census files downloaded from from [American Community Survey](https://www.census.gov/programs-surveys/acs)
* Obesity data downloaded from the [500 cities](https://www.cdc.gov/500cities/index.htm) project
* Shapefiles for plotting census tracts of Los Angeles, Memphis, Seattle-Tacoma-Bellevue and San Antonio, downloaded from various sources
* R and Python scripts for preparing data and running the models
* Output files generated from the prediction models

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### How to generate plots that appear in the paper

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

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
