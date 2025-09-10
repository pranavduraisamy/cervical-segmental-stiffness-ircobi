# *Comparison of Flexion-Extension Responses between Male and Female sub-Axial Cervical Spine Segments*

## Abstract

&emsp;&emsp;While finite element human body models enable virtual representation of diverse populations, validation of female models remains a challenge due to limited sex-differentiated experimental data. We modelled the segmental rotation of C3-C7 cervical spine segments at a flexion and extension load of 3 Nm using Bayesian linear regression. Results showed sex-dependent asymmetry in flexion and extension. In male segments, the differences between flexion and extension was minimal, while female segments exhibited greater flexibility in flexion (approximately 4° difference). When comparing flexion and extension separately, the rotation of male and female segments in extension tend to be similar. However, for flexion, the female rotation was 4.5° more than male in average. These findings suggest that female cervical spines may not be a volumetrically scaled version of male spines. The observed sexual dimorphism likely results from the asymmetry in load-bearing structures of the cervical vertebrae, where the articular processes limit the rotation in extension while there is no similar skeletal obstruction in flexion. The findings provide information for development and validation of HBM lineups that represent both the sexes. This may be particularly relevant to investigating neck injuries in low-speed crashes where the kinematics tend to be close to physiological ranges. Despite limitations in sample size and unavailability of spinal measurements, through the use of a Bayesian approach that considers uncertainties in the analysis, this study provides insights to inform the development of more accurate sex-differentiated physical and virtual models.

**_Keywords_**:	Bayesian regression, cervical spine, segmental rotations, sex-differences, sexual dimorphism. 

## Tree
```
cervical-segmental-stiffness-ircobi/main/
├───data
│   ├───Nightingale2002
│   │   ├───clean-data          # Data catalog and Master data
│   │   ├───code                # Codes used for extraction from NHTSA and creating of master dataframe
│   │   └───raw
│   │       ├───ascii           # ASCII files (unzipped from extracted folder)
│   │       ├───extracted       # Downloaded files from NHTSA
│   │       └───pdf-reports     # Test Reports
│   ├───Nightingale2007
│   │   ├───clean-data          # Data catalog and Master data
│   │   ├───code                # Codes used for extraction from NHTSA and creating of master dataframe
│   │   └───raw
│   │       ├───ascii           # ASCII files (unzipped from extracted folder)
│   │       ├───extracted       # Downloaded files from NHTSA
│   │       └───pdf-reports     # Test Reports
│   └───Winkelstein2000
│       ├───clean-data          # Data extracted from appendix
│       ├───code                # Codes used for extraction from the appendix (paper in .pdf format)
│       └───raw                 # Paste the pdf here before running the code
└───studies
    ├───code                    # EDA Plots and Bayesian model
    └───processed-data          # Data used in the model, inference data pickle file
```
## Required modules
```
arviz==0.17.1
arviz_plots==0.4.0
arviz_stats==0.5.0.dev0
bambi==0.14.0
great_tables==0.13.0
holoviews==1.20.2
matplotlib==3.8.4
numpy==1.26.4
pandas==2.2.2
pathlib==1.0.1
pickle
requests==2.32.3
tabula
xarray==2025.1.2
zipfile
```
## Links

|[Publication](https://www.ircobi.org/wordpress/downloads/irc25/pdf-files/25115.pdf)|[Presentation](https://pranavduraisamy.github.io/cervical-segmental-stiffness-ircobi/presentation.html)|
| ------------- | ------------- |
