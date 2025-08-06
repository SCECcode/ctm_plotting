#!/usr/bin/env python
#
#  query_2d_cross_section.py
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
from calculate_geodesic_track import calculate_geodesic_track
from write_csv_output import write_csv_output

## query the model along a vertical cross-section between lon/lat pairs
#  - inputs: start longitude and latitude, end longitude and latitude, start and end depth, and model name; optional plotting
#  - returns: DataFrame with temperature at these points; optional figure
def query_2D_vertical_cross_section(lat_start, lon_start, lat_end, lon_end, z_start, z_end, modelname, plot=False):
    
    # initialize dataset
    xdata = init_ctm(modelname)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon_start, lon_end], 
                                  "latitude[°]": [lat_start, lat_end], 
                                  "depth[m]": [z_start, z_end]})

    # calculate lon/lat points along a track
    ntrack = 121
    glons, glats = calculate_geodesic_track(lon_start, lat_start, lon_end, lat_end, ntrack)
    
    # define depth range
    ndep = 61
    zvals = np.linspace(z_start, z_end, ndep)

    # interpolate along track and vertically
    xi = xdata.interp({"longitude[°]": xr.DataArray(glons, dims="track index"), 
                  "latitude[°]": xr.DataArray(glats, dims="track index"),
                  "depth[m]": zvals})

    
    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[["longitude[°]", "latitude[°]", "depth[m]", "temperature[°C]"]]

    # return
    if plot: # optional plot
        fig = test_plot(xi, "2D_vertical")
        return df, fig
    else:
        return df

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    lat_start = float(input('Enter the starting latitude (°): '))
    lon_start = float(input('Enter the starting longitude (°): '))
    lat_end = float(input('Enter the ending latitude (°): '))
    lon_end = float(input('Enter the ending longitude (°): '))
    z_start = float(input('Enter the starting depth (m): '))
    z_end = float(input('Enter the ending depth (m): '))
    modelname = str(input('Enter model name (Lee_2025 or Shinevar_2018): '))

    # Call the function
    df = query_2D_vertical_cross_section(
        lat_start,
        lon_start,
        lat_end,
        lon_end,
        z_start,
        z_end,
        modelname)

    write_csv_output(df, f'2D_vertical_cross_section_{modelname}.csv', '2D_vertical', modelname)
