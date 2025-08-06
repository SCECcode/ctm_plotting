#!/usr/bin/env python
#
#  query_2d_horizontal_slice.py
#

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr

# Import initiation functions
from Initiation import init_ctm 
from Value_check import check_inbounds_values
from test_plot import test_plot
from write_csv_output import write_csv_output

## query the model along a horizontal slice at fixed depth
#  - inputs: start longitude and latitude, end longitude and latitude, slice depth; optional plotting
#  - returns: DataFrame with temperature at these points; optional figure
def query_2D_horizontal_slice(lat_start, lon_start, lat_end, lon_end, z_slice, modelname, plot=False):
    
    # initialize dataset
    xdata = init_ctm(modelname)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon_start, lon_end], 
                                  "latitude[°]": [lat_start, lat_end], 
                                  "depth[m]": [z_slice]})
    
    # define longitude and latitude arrays for the slice sample
    nlon, nlat = 101, 101
    lon_vals = np.linspace(lon_start, lon_end, nlon)
    lat_vals = np.linspace(lat_start, lat_end, nlat)

    # sample the horizontal slice at fixed depth
    xi = xdata.interp({"longitude[°]": lon_vals, "latitude[°]": lat_vals, "depth[m]": z_slice})

    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[["longitude[°]", "latitude[°]", "depth[m]", "temperature[°C]"]]

    # return
    if plot: # optional plot
        fig = test_plot(xi, "2D_horizontal")
        return df, fig
    else:
        return df

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    lat_start = float(input('Enter the starting latitude (°): '))
    lon_start = float(input('Enter the starting longitude (°): '))
    lat_end = float(input('Enter the ending latitude (°): '))
    lon_end = float(input('Enter the ending longitude (°): '))
    z = float(input('Enter the slice depth (m): '))
    modelname = str(input('Enter model name (Lee_2025 or Shinevar_2018): '))

    # Call the function
    df = query_2D_horizontal_slice(
        lat_start,
        lon_start,
        lat_end,
        lon_end,
        z,
        modelname)

    write_csv_output(df, f'2D_horizontal_slice_{modelname}.csv', '2D_horizontal', modelname)
