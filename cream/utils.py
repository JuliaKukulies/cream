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



def time_avg(xr_obj):
    """ This function averages all variables in xarray dataset along the time axis"""

    return avg










