"""
This :code: 'dataproducts' module provides classes which represent the different data types of ERA5.

ERA5(): parent class, contains several functions to download the data from Copernicus server: https://cds.climate.copernicus.eu/

Surface(ERA5): ERA5 data on single level from ECMWF

Pressure(ERA5):ERA5 data on 37 pressure levels (1000 hpa to 1 hpa) from ECMWF

"""

import cdsapi
import os
import numpy as np

class ERA5(object):
    """
    Base class for ERA5 data products.

    This class provides an interface to facilitate the download of ERA5 data products from Copernicus. 


    Attributes:
    -----------
    product(str): supported products are land, single-level, pressure-levels
    resolution(str): hourly or monthly 
    variables(list): list with ERA5 variable(s) (check https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation for all available variables)
    domain(str): select region with "lat2/lon1/lat1/lon2", if None: global data is downloaded
    path(str): name of directory where data download is stored: cache/
    """

    def __init__(self, product, variables, resolution, domain= None ):
        self.product = product
        self.resolution = resolution 
        self.variables = variables
        if domain == None:
            self.domain= ""
        else:
            self.domain = domain

        # create output directory to store data downloads, if it does not already exist
        self.path = 'cache'
        if os.path.isdir(self.path) ==  False :
            os.mkdir(self.path)

    def get_data_per_year(self, years, months = None, days = None, hours = None):
        """Downloads ERA5 data for a specific year or multiple years at hourly or monthly resolution. The output data is stored seperately for each year.

        Parameter:
        ----------

        years(list): string list with year(s) to download at hourly or monthly resolution

        optional:
        ----------

        months(list): string list with months, if None: all months are downloaded
        days(list): string list with days, if None: all days are downloaded
        hours(list): string list with hours, if None: all hours are downloaded for hourly data and monthly means 
        """

        # open new client instance
        c = cdsapi.Client()

        # check with data product to download 
        if self.resolution == 'monthly':
            downloadkey = self.product + '-monthly-means'
            if hours == None:
                producttype= 'monthly_averaged_reanalysis'
        else:
            producttype= 'reanalysis'
            downloadkey = self.product

        # select all months, days and hours if not specifies
        if months == None:
            months=   list(np.arange(1,13).astype(str))

        if days == None:
            days =  list(np.arange(1,32).astype(str))

        if hours == None:
            hours = list(np.arange(0,24).astype(str))

        # download data for each year
        for year in years:
            filename= 'era5_'+ downloadkey +'_'+ year +  '.nc'
            filepath = os.path.join(self.path, filename)

            # check whether file already has been downloaded
            if os.path.exists('cache/'+filename) == True:
                print('omittted download for ', filename)

            else:
                # send API request for data download
                c.retrieve('reanalysis-era5-'+ downloadkey , {
                    "product_type":   producttype,
                    "format":         "netcdf",
                    "area":           self.domain, 
                    "variable":       self.variables,
                    "year":           year,
                    "month":          months,
                    "day":           days,
                    "time":          hours
                }, filepath)

                print('file downloaded and saved as ', filepath)


    def get_data_for_composites(self, composites):
        """Downloads ERA5 data for hourly (non-consecutive) timesteps, where each timestep is saved as a separate file. Since the timesteps do not need to be consecutive, the function enables the download for climate composites.

        Parameter:
        ----------

        composites(dict): dictionary with years, months, days and hours in datetime format for timesteps

        """
        # open new client instance
        c = cdsapi.Client()

        for i,year in enumerate(composites['years']):
            year = str(year)
            month= str(composites['months'][i])
            day= str(composites['days'][i])
            hour= str(composites['hours'][i])

            filename = 'era5_'+ self.product+'_'+ year + month + day + hour+ '.nc'
            filepath = os.path.join(self.path, filename)

            # Send request (download data)
            c.retrieve('reanalysis-era5-'+self.product, {
                "product_type":   "reanalysis",
                "format":         "netcdf",
                "area":           self.domain,
                "variable":       self.variables,
                "year":           [year],
                "month":          [month],
                "day":            [day],
                "time":           [hour]
            }, filepath)

            print('file downloaded and saved as', filepath)

    # def get_data_for_range():









class Surface(ERA5):
    """

    Surface is a child class of ERA5 data products, which describes products with surface or column-integrated data. Each timestep contains two-dimensional data points. 

    """
    def __init__(self):
        ERA5.__init__(self, product, variables, domain, dimension)





class Pressure(ERA5):
    """
    Pressure a child class of ERA5 data products, which describes data at different pressure levels in the atmosphere. Each timestep contains three-dimensional data points. 


    """
    def __init__(self):
        ERA5.__init__(self, product, variables, domain, dimension)













