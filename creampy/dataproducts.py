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
from creampy import plotting
from creampy import utils



class ERA5():
    """
    Class for with metadata for different ERA5 data products. This class provides an interface to facilitate the download of ERA5 data products from the Copernicus server. 


    Attributes:
    -----------
    product(str): supported products are land, single-level, pressure-level
    resolution(str): hourly or monthly
    variables(list): list with ERA5 variable(s) (check https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation for all available variables)
    domain(list): list with strings to select region  [lat2,lon1,lat1,lon2], if None: global data is downloaded
    path(str): name of directory where data download is stored: cache/
    files(list): list with file paths, once the data for a specific data product and subsetting is has been downloaded 
    """

    def __init__(self, product, variables, resolution, domain= None):
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

        self.files = [] 

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
            filename= 'era5_'+ downloadkey +'_'+ year + m + d + h + '_' +''.join(self.variables) + '_' + ','.join(self.domain)+   '.nc'
            filepath = os.path.join(self.path, filename)

            # check whether file already has been downloaded
            if os.path.exists(filepath) == True:
                print('omittted download for ', filename)

            else:
                # send API request for data download
                c.retrieve('reanalysis-era5-'+ downloadkey , {
                    "product_type":   producttype,
                    "format":         "netcdf",
                    "area":           '/'.join(self.domain), 
                    "variable":       self.variables,
                    "year":           year,
                    "month":          months,
                    "day":           days,
                    "time":          hours
                }, filepath)

                print('file downloaded and saved as ', filepath)
                self.files.append(filepath)



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

            filename = 'era5_'+ self.product+'_'+ year + month + day + hour+'_' + ''.join(self.variables) +  '_' + ','.join(self.domain)+  '.nc'
            filepath = os.path.join(self.path, filename)

            # check whether file already has been downloaded
            if os.path.exists(filepath) == True:
                print('omittted download for ', filename)

            else:
                # Send request (download data)
                c.retrieve('reanalysis-era5-'+self.product, {
                    "product_type":   "reanalysis",
                    "format":         "netcdf",
                    "area":            '/'.join(self.domain),
                    "variable":       self.variables,
                    "year":           [year],
                    "month":          [month],
                    "day":            [day],
                    "time":           [hour]
                }, filepath)

                print('file downloaded and saved as', filepath)
                self.files.append(filepath)




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

            if start.year != end.year:

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

            else:
                months = np.arange(start.month, end.month + 1 ).astype(str)
                nr_of_months = np.shape(months)[0]
                years = [str(start.year)] * nr_of_months



            for idx,month in enumerate(months):
                year = years[idx]
                filename = 'era5_'+ downloadkey +'_'+ year +  month +'_' + ''.join(self.variables) + '_' + ','.join(self.domain)+ '.nc'
                filepath = os.path.join(self.path, filename)

                # check whether file already has been downloaded
                if os.path.exists(filepath) == True:
                    print('omittted download for ', filename)

                else:
                        # API request for specific year and month 
                        c.retrieve('reanalysis-era5-'+downloadkey, {
                            "product_type":   "monthly_averaged_reanalysis",
                            "format":         "netcdf",
                            "area":            '/'.join(self.domain),
                            "variable":       self.variables,
                            "year":           [year],
                            "month":          [month],
                            "time":            ['00:00'],
                        }, filepath)

                        print('file downloaded and saved as', filepath)
                        self.files.append(filepath)

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

                filename = 'era5_'+ self.product +'_'+ year +  month + day+ hour+ '_' + ''.join(self.variables) + '_' + ','.join(self.domain) +  '.nc'
                filepath = os.path.join(self.path, filename)

                # check whether file already has been downloaded
                if os.path.exists(filepath) == True:
                    print('omittted download for ', filename)

                else:
                        # API request for specific year and month 
                        c.retrieve('reanalysis-era5-'+ self.product , {
                            "product_type":   "reanalysis",
                            "format":         "netcdf",
                            "area":           '/'.join(self.domain),
                            "variable":       self.variables,
                            "year":           [year],
                            "month":          [month],
                            "day" :           [day],
                            "time":           [hour],
                        }, filepath)

                        print('file downloaded and saved as', filepath)
                        self.files.append(filepath)



    def get_files(self):
        import glob
        if len(self.variables) > 1:
            vars = self.variables[0]  + self.variables[-1]
        else:
            vars = self.variables[0]

        self.files = glob.glob('cache/*'+ self.product  +'*' +  vars +'*'+ ','.join(self.domain) + '.nc')
        return self.files






class Surface():
    """

    The Surface class contains data with surface or column-integrated data, when reading in a netCDF file of ERA5. Each timestep contains two-dimensional data points.
    The class is a child class of xarrray Dataset, which makes it possible to access all data, which is saved in the netcdf files from ERA5. 

    Parameter:
    ----------
    xr_obj : xarray Dataset object

    Attributes:
    -------------
    obj: is the data object of xarray Dataset with all its attributes. Data can be accessed the same way as for xarray Dataset objects via this attribute.


    Examples to access xarray attributes:
    ----------

    self.obj.dims: dimensions of dataset 
    self.obj.latitude.values : numpy array with latitude values

    """
    def __init__(self,  xr_obj):
        self.obj = xr_obj

    def get_coords(self):
        """
        Returns:

        lons(float32): array with longitudes 
        lats(float32): array with latitudes 

        """
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values
        return lons, lats 

    def create_wind_plot(self,  out = None ):
        """
        This function creates a map with surface wind vectors and wind speeds from u and v wind components of surface data. 
        """
        u = self.obj.u100.values[0,::]
        v= self.obj.v100.values[0,::]
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values
        plotting.plot_surface_wind(lons, lats, u, v, out = out)


    def create_map(self, variable, out = None):
        """
        This function creates a map of a any chosen climate variable from surface/ single-level data. 

        Parameters:
        ------------

        var(str): short name of variable to plot 

        """
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values

        var = self.obj[variable].values[0]
        unit= str(self.obj[variable].units)
        varname = str(self.obj[variable].long_name)


        plotting.plot_map(lons, lats, var,varname, unit, out = out )



    def create_contour_map(self, variable, out = None, filled= None, levels = None):
        """
        This function creates a map of a any chosen climate variable from surface/ single-level data. 

        Parameters:
        ------------

        var(str): short name of variable to plot

        optional:

        filled (boolean): if True, contours with filled regions will be created. The default creates contour lines.
        levels : array containing the variable values for which contours are drawn

        """
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values

        var = self.obj[variable].values[0]
        unit= str(self.obj[variable].units)
        varname = str(self.obj[variable].long_name) 
        plotting.plot_contours(lons, lats, var, varname, out = out , filled = filled, levels = levels)




class Pressure():
    """
    The Pressure class contains data at different pressure levels in the atmosphere, when reading in a netCDF file of ERA5. Each timestep contains three-dimensional data points.
    The class is a child class of xarrray Dataset, which makes it possible to access all data, which is saved in the netcdf files from ERA5. 

    Parameter:
    ----------
    xr_obj : xarray Dataset object

    Attributes:
    -------------
    obj: is the data object of xarray Dataset with all its attributes. Data can be accessed the same way as for xarray Dataset objects via this attribute.


    Examples to access xarray attributes:
    ----------

    self.obj.dims: dimensions of dataset
    self.obj.latitude.values : numpy array with latitude values


    """
    def __init__(self,  xr_obj):
        self.obj = xr_obj


    def get_coords(self):
        """
        Returns:

        lons(float32): array with longitudes 
        lats(float32): array with latitudes 

        """

        lons = self.obj.longitude.values
        lats = self.obj.latitude.values
        return lons, lats


    def create_synoptic_plot(self,  pl, out = None ):
        """ This function creates a synoptic map at a chosen pressure level to display upper-level wind circulation and geopotential height. 
        """
        u = self.obj.u.values[0,::]
        v= self.obj.v.values[0,::]
        geopotential= self.obj.z.values[0,::]
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values
        plotting.plot_synoptic(lons, lats, u, v, geopotential, pl, out = out)




    def create_map(self, variable, level, out = None):
        """
        This function creates a map of a any chosen climate variable from surface/ single-level data. 

        Parameters:
        ------------

        var(str): short name of variable to plot 
        level(str): pressure level or 'column-integrated' to calculated the mean value through the atmospheric column 


        """
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values

        if level == 'column-integrated':
            var = utils.column_integration(self.obj[variable].values[0],  self.obj.z.values[0])
        else:
            level_idx = np.where(self.obj.level.values== level)[0]
            var = self.obj[variable].values[0, level_idx , :, :][0]

        unit= str(self.obj[variable].units)
        varname = str(self.obj[variable].long_name)
        plotting.plot_map(lons, lats, var,varname, unit, out = out )



    def create_contour_map(self, variable, level,  out = None, filled= None, levels = None):
        """
        This function creates a map of a any chosen climate variable from surface/ single-level data. 

        Parameters:
        ------------

        var(str): short name of variable to plot
        level(str): pressure level or 'column-integrated' to calculated the mean value through the atmospheric column

        optional:

        filled (boolean): if True, contours with filled regions will be created. The default creates contour lines.
        levels : array containing the variable values for which contours are drawn

        """
        lons = self.obj.longitude.values
        lats = self.obj.latitude.values


        if level == 'column-integrated':
            var = utils.column_integration(self.obj[variable].values[0],  self.obj.z.values[0])
        else:
            level_idx = np.where(self.obj.level.values== level)[0]
            var = self.obj[variable].values[0, level_idx , :, :][0]

        var = self.obj[variable].values[0]
        unit= str(self.obj[variable].units)
        varname = str(self.obj[variable].long_name) 
        plotting.plot_contours(lons, lats, var, varname, unit= unit, out = out , filled = filled, levels = levels)




    def create_vertical_plot(self, variable, dim, unit = None, out = None):
        """This function creates a 2D map for any chosen climate variable.

        Parameter:
        ------------

        var (numpy.array) : any climate variable for one timestep (2-dimensionsal)
        dim (str): 'longitude' or 'latitude' for latitudinal or longitudinal cross section 


        optional:

        unit(str) : unit of climate variable 
        out (str): name of output file"""


        p_levels = self.obj.level.values

        if dim== 'latitude':
            coords = self.obj.latitude.values
        if dim == 'longitude':
            coords = self.obj.latitude.values

        var = utils.dim_average(self.obj, variable, dim)
        var = var[0]

        unit= str(self.obj[variable].units)
        varname = str(self.obj[variable].long_name)
        plotting.plot_vertical(coords, p_levels, var, varname, dim, unit = None, out = None)







