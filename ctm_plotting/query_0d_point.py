#!/usr/bin/env python
#
#  query_0d_point.py
#

from pyctm import init_ctm, check_inbounds_values

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import json
import argparse

## Query the model at a single point
#  - Inputs: latitude, longitude, depth to query model, modelname, input model path, and output JSON file path (optional)
#  - Returns: None. Create a JSON file if output path is defined
def query_0D_point(lat, lon, dep, modelname, modelpath):

    # initialize dataset
    xdata = init_ctm(modelname, modelpath)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep]})

    # interpolate a single point
    temp = float(xdata.interp({"longitude[°]": lon, "latitude[°]": lat, "depth[m]": dep})["temperature[°C]"])

    # return in DataFrame format
    return pd.DataFrame({"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep], "temperature[°C]": [temp]})

def call_func():
    
    par = argparse.ArgumentParser()
    par.add_argument('--lat', type = float, required = True)          # Add argument of latitude (°)
    par.add_argument('--lon', type = float, required = True)          # Add argument of longitude (°)
    par.add_argument('--z', type = float, required = True)            # Add arugment of depth (m)
    par.add_argument('--modelname', type = str, required = True)      # Add argument of model name: Lee_2025 or Shinevar_2018
    par.add_argument('--modelpath', type = str, required = True)      # Add argument of input model path
    par.add_argument('--outpath', type = str, required = False)       # Add argument of output file path and file name
    args = par.parse_args()                                           # Extract arguments
    
    # Call the function
    df = query_0D_point(
        args.lat,
        args.lon,
        args.z,
        args.modelname,
        args.modelpath)

    # Rename df column name
    rename = {'longitude[°]': 'lon',
              'latitude[°]': 'lat',
              'depth[m]': 'Z',
              'temperature[°C]': 'temp'}
    df = df.rename(columns = rename)

    # Make it become a dictionary
    df_dict = df.iloc[0].to_dict()

    # Append model name to the output
    if args.modelname == 'Lee_2025':
        df_dict['model'] = 'lee25'
    else:
        df_dict['model'] = 'shinevar18'
        
    # Save as json file
    if args.outpath:
        with open(args.outpath, 'w') as f:
            json.dump(df_dict, f, separators = (',', ':'))
    # Or just print it if didn't define output path
    else:
            print(json.dumps(df_dict, separators = (',', ':')))

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    # Call the query function
    call_func()
