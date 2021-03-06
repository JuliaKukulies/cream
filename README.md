# Climate REanalysis Maps (CREAM)

This is a coding project within the scope of the Advanced Scientific Programming Course at Uppsala University. 
The aim is to **create a python package cream**, which can be used to search for, download, manipulate and plot climate reanalysis data 
for a chosen region. More specifically, different data products of ERA5 from https://climate.copernicus.eu/climate-reanalysis
will be represented by different classes in the package (surface and pressure level data )and the main functions should be to download data at different resolutions, calculate climatological means for chosen variables and then to create nice maps with cartopy, which can be used for climate data analysis. The idea is also to allow the package to be extended in the future, e.g. by adding different data products which can be downloaded from other servers than Copernicus. 

As a starting point for this coding project, I will use some old jupyter-notebooks from my research project, in which I have analyzed a specific 
dataset of ERA5 (at hourly resolution) and created maps. Since this type of data analysis and especially the creation of maps for a different datasets 
is a common tool in my research, I would like to make my code more general and organized, so that I can use the same functions for different datasets. 
Another thing I would like to improve in my code is the **documentation**. So in this project, I also would like to add proper descriptions of the functions 
in the package. 



