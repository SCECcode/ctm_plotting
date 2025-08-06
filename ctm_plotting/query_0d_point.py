#!/usr/bin/env python
#
#  query_0d_point.py
#

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
from pyproj import Geod

# Import initiation functions
from Initiation import init_ctm
from Value_check import check_inbounds_values

## query the model at a single point
#  - inputs: latitude, longitude, depth to query model, modelname
#  - returns: DataFrame with temperature at this point
def query_0D_point(lat, lon, dep, modelname):

    # initialize dataset
    xdata = init_ctm(modelname)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep]})

    # interpolate a single point
    temp = float(xdata.interp({"longitude[°]": lon, "latitude[°]": lat, "depth[m]": dep})["temperature[°C]"])

    # return in DataFrame format
    return pd.DataFrame({"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep], "temperature[°C]": [temp]})

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    lat = float(input('Enter the latitude (°): '))
    lon = float(input('Enter the longitude (°): '))
    z = float(input('Enter the depth (m): '))
    modelname = str(input('Enter model name (Lee_2025 or Shinevar_2018):'))

    # Call the function
    df = query_0D_point(
        lat,
        lon,
        z,
        modelname)

    print(df)
