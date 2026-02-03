#!/usr/bin/env python
#
#  query_1d_depth_profile.py
#

from pyctm import init_ctm, check_inbounds_values, test_plot, write_csv_output

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import argparse
from pyproj import Geod

## query the model along a vertical profile with fixed longitude and latitude
#  - inputs: longitude, latitude, depths (start, stop, and step), model name to query; option to plot
#  - returns: DataFrame with temperature at these points; optional figure
def query_1D_vertical_profile(lat, lon, z_start, z_end, z_step, modelname, modelpath, plot = False):
    
    # initialize dataset
    xdata = init_ctm(modelname, modelpath)

    # Boyd (2019) model does not start at the surface (depth = 0 meter). Here I have to extrapolate to get the surface temperature.
    if modelname == 'Boyd_2019':
        surface = np.insert(xdata['depth[m]'].values, 0, 0)
        xdata = xdata.interp({'depth[m]': surface}, method = 'linear', kwargs = {'fill_value': 'extrapolate'})

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [z_start, z_end]})
    zvals = np.arange(z_start, z_end+z_step/10.0, z_step)
    xi = xdata.interp({"longitude[°]": lon, "latitude[°]": lat, "depth[m]": zvals})

    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[['longitude[°]', 'latitude[°]', 'depth[m]', 'temperature[°C]']]

    # return    
    if plot: # optional plot
        fig = test_plot(xi, '1D_vertical')
        return df, fig
    else:
        return df

# Make a function to allow batch mode
def call_func():
    
    par = argparse.ArgumentParser()
    par.add_argument('--lat', type = float, required = True)          # Add argument of latitude (°)
    par.add_argument('--lon', type = float, required = True)          # Add argument of longitude (°)
    par.add_argument('--z_start', type = float, required = True)      # Add arugment of starting depth (m)
    par.add_argument('--z_end', type = float, required = True)        # Add arugment of ending depth (m)
    par.add_argument('--z_step', type = float, required = True)       # Add arugment of depth interval (m)
    par.add_argument('--modelname', type = str, required = True)      # Add argument of model name: Lee_2025 or Shinevar_2018
    par.add_argument('--modelpath', type = str, required = True)      # Add argument of input model path
    par.add_argument('--outpath', type = str, required = True)        # Add argument of output file path and file name
    
    args = par.parse_args()                                           # Extract arguments
    
    # Call the function
    df = query_1D_vertical_profile(
         args.lat,
         args.lon,
         args.z_start,
         args.z_end,
         args.z_step,
         args.modelname,
         args.modelpath)

    df.drop(columns = ['longitude[°]', 'latitude[°]'], inplace = True)

    # Rename columns
    rename = {'depth[m]': '# Depth(m)',
              'temperature[°C]': 'Temperature(°C)'}
    
    df = df.rename(columns = rename)

    final_outpath = args.outpath[:]
    final_outpath.replace('data','data_final',1)
    write_csv_output(df, final_outpath, '1D_vertical', args.modelname, longitude = args.lon, latitude = args.lat)

    # Add dummy columns
    df[['dummy1', 'dummy2']] = np.nan
    
    # Call the function to write the output csv file
    write_csv_output(df, args.outpath, '1D_vertical', args.modelname, longitude = args.lon, latitude = args.lat)

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    # Call the query function
    call_func()
