"""Utility (general-purpose) functions for python package **cream**  """


import numpy as np

def geopotential_to_height(z):
    """ This function converts geopotential heights to geometric heights. This approximation takes into account the varying gravitational force with heights, but neglects latitudinal vairations.


    Parameters:
    ------------

    z(float) : (1D or multi-dimenstional) array with geopotential heights

    Returns:
    ----------

    geometric_heights : array of same shape containing altitudes in metres

    """
    g = 9.80665 # standard gravity 
    Re = 6.371 * 10**6  # earth radius
    geometric_heights   = (z*Re / (g * Re - z))

    return geometric_heights 


def column_integration(values, z, ax = None ):
    """This functions calculates the column-integrated value of a given atmospheric variable at different pressure levels


    Parameters:
    -----------

    values(float): 1D or multi-dimensional array with values of atmospheric variable at different pressure levels
    z(int): array with geopotential heights for values
    axis = axis along which to integrated. The default is 0.


    Returns:
    --------

    colint(float): array with column-integrated values of variable (dimension reduced by 1)
    """
    # convert geopotential to geometric heights
    geometric_heights   = geopotential_to_height(z)

    if ax == None:
        ax = 0

    # integration of column values
    colint = np.trapz(values, geometric_heights, axis =ax )

    return colint



def dim_average(xr_obj, var, dim):
    """ This function averages a climate variable from an xarray dataobject along a specified dimension.

    Parameters:
    -----------

    xr_obj: xrray Dataset object
    var (str): short name of variable in of xr_obj
    dim (str): name of dimension over which the average should be taken


    Returns:
    --------

    avg: array with reduced dimension, containing the averages along time, latitudes or longitudes 

    """

    data = xr_obj[var].values
    ax = np.where(np.array(xr_obj[var].dims) == dim)[0][0]
    avg = np.nanmean(data, axis = ax)

    return avg































