#!/usr/bin/env python
#
#  query_1d_depth_profile.py
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
from test_plot import test_plot
from write_csv_output import write_csv_output

## query the model along a vertical profile with fixed longitude and latitude
#  - inputs: longitude, latitude, depths (start, stop, and step), model name to query; option to plot
#  - returns: DataFrame with temperature at these points; optional figure
def query_1D_vertical_profile(lat, lon, z_start, z_end, z_step, modelname, plot=False):
    
    # initialize dataset
    xdata = init_ctm(modelname)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [z_start, z_end]})
    zvals = np.arange(z_start, z_end+z_step/10.0, z_step)
    xi = xdata.interp({"longitude[°]": lon, "latitude[°]": lat, "depth[m]": zvals})

    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[["longitude[°]", "latitude[°]", "depth[m]", "temperature[°C]"]]

    # return
    if plot: # optional plot
        fig = test_plot(xi, "1D_vertical")
        return df, fig
    else:
        return df

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    lat = float(input('Enter the latitude (°): '))
    lon = float(input('Enter the longitude (°): '))
    z_start = float(input('Enter the starting depth (m): '))
    z_end = float(input('Enter the ending depth (m): '))
    z_step = float(input('Enter the depth interval (m): '))
    modelname = str(input('Enter model name (Lee_2025 or Shinevar_2018): '))

    # Call the query function
    df = query_1D_vertical_profile(
        lat,
        lon,
        z_start,
        z_end,
        z_step,
        modelname)

    write_csv_output(df, f'1D_vertical_profile_{modelname}.csv', '1D_vertical', modelname)
