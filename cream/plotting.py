"""The :code: 'plotting' module provides some basic plotting functions, to create fancy maps based on gridded climate data. 

"""

import os 
import cartopy
import quiver
import cartopy.feature as cfeat
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np


def plot_surface_wind(lons, lats, u, v, out = None):
    """This function creates a surface wind maps showing both wind vectors and wind speed.

    Parameter:
    ------------

    lons (numpy.array) : longitudes of data object
    lats (numpy.array) : latitudes of data object
    u_wind (numpy.array) : u wind component for one timesteps (pressure levels )
    v_wind (numpy.array) :v wind component for one timestep (pressure levels)
    """


    # create output directory for plots if not existing
    plotdir = 'plots'
    if os.path.isdir(plotdir) ==  False :
            os.mkdir(plotdir)

    # convert coords to 2d array
    x,y = np.meshgrid(lons, lats)

    plt.figure(figsize= (18,9))

    # create axes
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([np.min(lons),np.max(lons), np.min(lats), np.max(lats)- 5])

    cmap = plt.cm.magma_r

    # calculate wind speed from u and v components:
    windspeed = (u ** 2 + v ** 2) ** 0.5

    # Plot geopotential
    m = plt.pcolormesh(lons,lats, windspeed, cmap = cmap)


    # Normalize the data for uniform arrow size
    u_norm = u/ np.sqrt(u ** 2.0 + v** 2.0)
    v_norm = v / np.sqrt(u ** 2.0 + v ** 2.0)


    # Plot wind vectors
    skip  =(slice(None,None,10),slice(None,None,10))
    plt.quiver(x[skip],y[skip],u_norm[skip], v_norm[skip], color ='k', transform= ccrs.PlateCarree())

    # colorbar
    cmap=plt.cm.viridis
    cbar= plt.colorbar(m, extend = 'both')
    cbar.set_label('wind speed (m$^2$ s$^{-1}$ )', fontsize = 15)


    # labels
    xlabels = np.linspace(int(np.min(lons)), int(np.max(lons)), 5)
    ylabels = np.linspace(int(np.min(lats)), int(np.max(lats)) , 8)
    plt.xticks(xlabels, xlabels, fontsize=20)
    plt.yticks(ylabels,ylabels, fontsize=20)
    plt.xlabel('Lon $^\circ$E',  fontsize=25)
    plt.ylabel('Lat $^\circ$N',  fontsize=25)

    # add extra features 
    ax.coastlines()

    if out == None:
        out ='surface_winds.png'

    plt.savefig(os.path.join(plotdir, out))
    plt.show()




def plot_synoptic(lons, lats, u, v, geopotential, pl, out = None  ):
    """This function creates a map to display the synoptic environment, which is represented as upper-level wind vectors together with geopotential height.

    Parameter:
    ------------

    lons (numpy.array) : longitudes of data object
    lats (numpy.array) : latitudes of data object
    u_wind (numpy.array) : u wind component for one timesteps (pressure levels )
    v_wind (numpy.array) :v wind component for one timestep (pressure levels)
    geopotential (numpy.array) : geopotential heights for one timestep (pressure levels)
    pl (int): pressure level (850,500 or 300)

    optional:
    pl (int): pressure level (850,500 or 300)
    out (str): name for output file

    """
    # create output directory for plots if not existing
    plotdir = 'plots'
    if os.path.isdir(plotdir) ==  False :
            os.mkdir(plotdir)

    # convert coords to 2d array
    x,y = np.meshgrid(lons, lats)

    # convert pressure level to index
    if pl == 850:
        level= 1
    if pl == 500:
        level = 3
    if pl == 300:
        level= 5

    plt.figure(figsize= (18,9))

    # create axes
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([np.min(lons),np.max(lons), np.min(lats), np.max(lats)- 5])

    cmap = plt.cm.viridis


    # Plot geopotential
    m = plt.pcolormesh(lons,lats, geopotential[level,:,:]/1000, cmap = cmap)


    # Normalize the data for uniform arrow size
    u_norm = u[level, :,:]/ np.sqrt(u[level,:,:] ** 2.0 + v[level,:,:] ** 2.0)
    v_norm = v[level, :,:] / np.sqrt(u[level, :,:] ** 2.0 + v[level,:,:] ** 2.0)


    # Plot wind vectors 
    skip  =(slice(None,None,10),slice(None,None,10))
    plt.quiver(x[skip],y[skip],u_norm[skip], v_norm[skip], color ='k', transform= ccrs.PlateCarree())

    # colorbar
    cmap=plt.cm.viridis
    cbar= plt.colorbar(m, extend = 'both')
    cbar.set_label('geopotential (km$^2$ s$^{-2}$ )', fontsize = 15)


    # labels
    xlabels = np.linspace(int(np.min(lons)), int(np.max(lons)), 5)
    ylabels = np.linspace(int(np.min(lats)), int(np.max(lats)) , 8)


    plt.xticks(xlabels, xlabels, fontsize=20)
    plt.yticks(ylabels,ylabels, fontsize=20)
    plt.xlabel('Lon $^\circ$E',  fontsize=25)
    plt.ylabel('Lat $^\circ$N',  fontsize=25)

    # add extra features
    ax.coastlines()

    if out == None:
        out ='synoptic.png'

    plt.savefig(os.path.join(plotdir, out))
    plt.show()









