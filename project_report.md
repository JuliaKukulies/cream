# Progress report for cream package: 

**Julia Kukulies** 


The following classes and methods have been implemented within the scope of the python project course (03 April, 2020). 


## DONE 

### classes

- class ERA5
- class Pressure 
- class Surface

### methods

- different download methods to obtain files 
- check for downloaded files in directory 
- plot surface winds 
- plot synopic environment 
- plot 2D map of any surface variable
- plot 2D map of any pressure variable 
- calculate column-integrated values from pressure levels 
- create maps with contour lines/regions 
- calculate averages along certain dimension (time, latitude or longitude)
- create plot of vertical cross section along latitudes or longitudes 


### additional

- tested all implemented functions
- created example notebook
- documentation with doc strings 


# Future extensions of the package could be:


## TODO 

### general extensions 
 
 - add more dataproduct classes (e.g. other climate reanalyses or gridded observation datasets)
 - more advances search functions in data, e.g. check for and extract for specific datapoints at specific time and location 
 - add utilities to information from different datasets 
 - sphynx documentation 
 - add package via PyPI (Python Package Index )
 

 
### methods
 
 
- create timeseries, animation of consecutive timesteps 
- more time handling utilities, calculate seasonal averages, etc (e.g. combine with some functions of command-line programm **Climate Data Operator**)
- calculate averages and  handle timesteps 
- calculate wind shear 
- calculate moisture flux convergence 

