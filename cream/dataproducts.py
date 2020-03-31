"""
This :code: 'dataproducts' module provides classes which represent the different data types of ERA5.

ERA5(): parent class, contains several functions to download the data from Copernicus server: https://cds.climate.copernicus.eu/

Surface(ERA5): ERA5 data on single level from ECMWF

Pressure(ERA5):ERA5 data on 37 pressure levels (1000 hpa to 1 hpa) from ECMWF

"""

import cdsapi
import os
import datetime
import numpy as np
import xarray


# import modules from the cream package
from cream import plotting



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
            m = ''
        else:
            # string for file name
            m= '_months' + ''.join(months)

        if days == None:
            days =  list(np.arange(1,32).astype(str))
            d= ''
        else:
            # string for file name
             d= '_days' + ''.join(months)

        if hours == None:
            hours = list(np.arange(0,24).astype(str))
            h= ''
        else:
            # string for filename
            h = '_hours' + ''.join(months)

        # download data for each year
        for year in years:
            filename= 'era5_'+ downloadkey +'_'+ year + m + d + h + '_' +''.join(self.variables) +  '.nc'
            filepath = os.path.join(self.path, filename)

            # check whether file already has been downloaded
            if os.path.exists(filepath) == True:
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

        composites: list with timesteps asy,  dateime format (containing year, month, day, hour for each timestep)

        """
        # open new client instance
        c = cdsapi.Client()

        for i in np.arange(0,len(composites)):
            year= str(composites[i].year)
            month= str(composites[i].month)
            day= str(composites[i].day)
            hour= str(composites[i].hour)

            filename = 'era5_'+ self.product+'_'+ year + month + day + hour+'_' + ''.join(self.variables) + '.nc'
            filepath = os.path.join(self.path, filename)

            # check whether file already has been downloaded
            if os.path.exists(filepath) == True:
                print('omittted download for ', filename)

            else:
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




    def get_data_for_range(self,start, end):
        """Download ERA5 for a given range.

        Parameter:
        ----------

        start(datetime.datetime): start time
        end(datetime.datetime): end time

        """

        # open new client instance
        c = cdsapi.Client()
        import itertools

        if self.resolution == 'monthly':

            downloadkey = self.product + '-monthly-means'

            # get years with complete nr. of months 
            full_years_range = range(start.year + 1 , end.year)
            full_years = list(itertools.chain.from_iterable(itertools.repeat(x, 12) for x in full_years_range))
            all_months = np.arange(1,13).astype(str)

            # get months of uncomplete years 
            months_first_year = list(np.arange((start.month + 1),13 ).astype(str))
            months_last_year =  list(np.arange(1, (end.month+1)).astype(str))

            # create lists for years with months
            years = [str(start.year)] * len(months_first_year) +  [str(f) for f in full_years]   +  [str(end.year)] * len(months_last_year) 
            months = months_first_year +  [str(m) for m in all_months ]  * len(full_years_range) +  months_last_year

            for idx,month in enumerate(months):
                year = years[idx]
                filename = 'era5_'+ downloadkey +'_'+ year +  month +'_' + ''.join(variables) + '.nc'
                filepath = os.path.join(self.path, filename)

                # check whether file already has been downloaded
                if os.path.exists(filepath) == True:
                    print('omittted download for ', filename)

                else:
                        # API request for specific year and month 
                        c.retrieve('reanalysis-era5-'+downloadkey, {
                            "product_type":   "monthly_averaged_reanalysis",
                            "format":         "netcdf",
                            "area":           self.domain,
                            "variable":       self.variables,
                            "year":           [year],
                            "month":          [month],
                            "time":            ['00:00'],
                        }, filepath)

                        print('file downloaded and saved as', filepath)


        else:
            # get list with all years, months, days, hours between two dates
            delta =(end - start)
            hour = delta/3600
            dates = []
            for i in range(hour.seconds + 1):
                h = start + datetime.timedelta(hours=i)
                dates.append(h)

            for idx,date in enumerate(dates):
                year = str(dates[idx].year)
                month = str(dates[idx].month)
                day = str(dates[idx].day)
                hour= str(dates[idx].hour) 

                filename = 'era5_'+ self.product +'_'+ year +  month + day+ hour+ '_' + ''.join(self.variables) + '.nc'
                filepath = os.path.join(self.path, filename)

                # check whether file already has been downloaded
                if os.path.exists(filepath) == True:
                    print('omittted download for ', filename)

                else:
                        # API request for specific year and month 
                        c.retrieve('reanalysis-era5-'+ self.product , {
                            "product_type":   "reanalysis",
                            "format":         "netcdf",
                            "area":           self.domain,
                            "variable":       self.variables,
                            "year":           [year],
                            "month":          [month],
                            "day" :           [day],
                            "time":           [hour],
                        }, filepath)

                        print('file downloaded and saved as', filepath)




class Surface(ERA5):
    """

    Surface is a child class of ERA5 data products, which describes products with surface or column-integrated data. Each timestep contains two-dimensional data points.

    """
    def __init__(self):
        ERA5.__init__(self, product, variables, domain, path)


class Pressure(ERA5):
    """
    Pressure a child class of ERA5 data products, which describes data at different pressure levels in the atmosphere. Each timestep contains three-dimensional data points.

    """
    def __init__(self, fname, variables, domain):
        ERA5.__init__(self, 'pressure-levels', variables, domain)
        self.fname = fname

        # read in data
        path_to_file = os.path.join(self.path, self.fname)
        data = xarray.open_dataset(path_to_file)

        # extract data from file 
        self.lons = data.longitude.values
        self.lats = data.latitude.values
        self.time= data.time.values[0]
        self.data = {}
        for name in variables:
            self.data[name] = data[name].values[0,:,:,:]


    def create_synoptic_plot(self,  pl, out = None ):
        try:
            u = self.data['u']
            v= self.data['v']
            geopotential= self.data['z']
        except:
            raise "pressure data does not contain wind vectors and/or geopotential data!"
        plotting.plot_synoptic( self.lons, self.lats, u, v, geopotential, pl)














