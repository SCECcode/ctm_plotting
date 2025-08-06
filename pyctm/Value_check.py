### Import package
import xarray as xr

## check if a query value is within model coordinates
#  - inputs: Xarray dataset, value to test, coordinate to test ("longitude", "latitude", "depth")
#  - returns: test result (True or false)
def check_inbounds_value(xdata, value, coord):

    # first, make sure this is a valid coordinate
    if coord in xdata.coords:
        
        # test for out of bounds value
        if (value < xdata[coord].min()) or (value > xdata[coord].max()):
            result = False
            raise ValueError("Error {:}={:} is out of model domain".format(coord, value))
        else:
            result = True

    # not a valid coordinate
    else:
        result = False
        raise NameError("{:} not in model coordinates".format(coord))

    # return result
    return result

## generalizes the function above to include multiple values and coordinates to test
#  - inputs: Xarray dataset, values to test as a dictionary of {coord: vals}
#  - returns: test result (True or false)
def check_inbounds_values(xdata, values):
    
    # initialize
    result = False

    # test all value / coordinate pairs
    for coord, vals in values.items():
        for val in vals:
            result = check_inbounds_value(xdata, val, coord)

    # return
    return result
