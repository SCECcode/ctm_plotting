
# Import package
import numpy as np
import pandas as pd

from pyctm import dTdz_2D_vertical_cross_section

## Compile CSV header information
#  - inputs: output dataframe, query type
#  - returns: header text
def get_csv_header(df, qtype, modelname):
    
    # common header for all types
    head = "# Title: CTM"

    # 1D vertical profile
    if qtype == "1D_vertical":  

        # extract data
        lon, lat = df["longitude[°]"].values[0], df["latitude[°]"].values[0]
        depths = np.sort(df["depth[m]"].unique())
        zstart, zend = depths[0], depths[-1]
        zspace = depths[1] - depths[0]
        dz = (depths[-1] - depths[0]) / 1000                              # Convert m to km
        dT = df["temperature[°C]"].max() - df["temperature[°C]"].min()    # Get temperature difference
        dTdz = dT / dz                                                    # Calculate geothermal gradient

        # write fields
        head += " 1D Profile\n"
        if modelname == 'Lee_2025':
            head += "# CTM(abbr): lee25\n"
        elif modelname == 'Shinevar_2018':
            head += "# CTM(abbr): shinevar18\n"
        head += "# Lat: {:.6f}\n# Lon: {:.6f}\n".format(lat,lon)
        head += "# Start_depth(m): {:.3f}\n".format(zstart)
        head += "# End_depth(m): {:.3f}\n".format(zend)
        head += "# Vert_spacing(m): {:.3f}\n".format(zspace)
        head += "# Average dT/dz(°C/km): {:.3f}\n".format(dTdz)
    
    # 2D horizontal slice
    elif qtype == "2D_horizontal":

        # extract data
        depth = df["depth[m]"].values[0]
        lons = np.sort(df["longitude[°]"].unique())
        lats = np.sort(df["latitude[°]"].unique())
        lon1, lon2 = lons[0], lons[-1]
        lat1, lat2 = lats[0], lats[-1]
        nlon, nlat = lons.size, lats.size
        npts = nlon * nlat
        Tmin = df["temperature[°C]"].min()
        Tmax = df["temperature[°C]"].max()
        Tmean = df["temperature[°C]"].mean()

        # write fields
        head += " Horizontal Slice at {:.3f} m depth\n".format(depth)
        if modelname == 'Lee_2025':
            head += "# CTM(abbr): lee25\n"
        elif modelname == 'Shinevar_2018':
            head += "# CTM(abbr): shinevar18\n"
        head += "# Data_type: T[°C]\n"
        head += "# Depth(m): {:.3f}\n".format(depth)
        head += "# Lon_pts: {:}\n".format(nlon)
        head += "# Lat_pts: {:}\n".format(nlat)
        head += "# Total_pts: {:}\n".format(npts)
        head += "# T Min: {:.6f}\n".format(Tmin)
        head += "# T Max: {:.6f}\n".format(Tmax)
        head += "# T Mean: {:.6f}\n".format(Tmean)
        head += "# Lat1: {:.6f}\n".format(lat1)
        head += "# Lat2: {:.6f}\n".format(lat2)
        head += "# Lon1: {:.6f}\n".format(lon1)
        head += "# Lon2: {:.6f}\n".format(lon2)
    
    # 2D vertical slice
    elif qtype == "2D_vertical":
        
        # extract data
        depths = np.sort(df["depth[m]"].unique())
        zstart, zend = depths[0], depths[-1]
        zspace = depths[1] - depths[0]
        nz = depths.size
        lons = df["longitude[°]"].unique()
        lats = df["latitude[°]"].unique()
        nlon, nlat = lons.size, lats.size
        lon1 = df.loc[0,"longitude[°]"]
        lon2 = df.loc[len(df)-1,"longitude[°]"]
        lat1 = df.loc[0,"latitude[°]"]
        lat2 = df.loc[len(df)-1,"latitude[°]"]
        nxy = len(df[["latitude[°]", "longitude[°]"]].drop_duplicates())
        npts = nxy * nz
        Tmin = df["temperature[°C]"].min()
        Tmax = df["temperature[°C]"].max()
        Tmean = df["temperature[°C]"].mean()
        df_dTdz = dTdz_2D_vertical_cross_section(df)
        dTdz_max = df_dTdz['dTdz[°C/km]'].max()

        # write fields
        head += " Cross Section from ({:.3f}, {:.3f}) to ({:.3f}, {:.3f})\n".format(lon1, lat1, lon2, lat2)
        if modelname == 'Lee_2025':
            head += "# CTM(abbr): lee25\n"
        elif modelname == 'Shinevar_2018':
            head += "# CTM(abbr): shinevar18\n"
        head += "# Data_type: T[°C]\n"
        head += "# Start_depth(m): {:.3f}\n".format(zstart)
        head += "# End_depth(m): {:.3f}\n".format(zend)
        head += "# Vert_spacing(m): {:.3f}\n".format(zspace)
        head += "# Depth_pts: {:}\n".format(nz)
        head += "# Horizontal_pts: {:}\n".format(nxy)
        head += "# Total_pts: {:}\n".format(npts)
        head += "# T Min: {:.6f}\n".format(Tmin)
        head += "# T Max: {:.6f}\n".format(Tmax)
        head += "# T Mean: {:.6f}\n".format(Tmean)
        head += "# Average dT/dz Max (°C/km): {:.6f}\n".format(dTdz_max)
        head += "# Num_x: {:}\n".format(nxy)
        head += "# Num_y: {:}\n".format(nz)
        head += "# Lat1: {:.6f}\n".format(lat1)
        head += "# Lat2: {:.6f}\n".format(lat2)
        head += "# Lon1: {:.6f}\n".format(lon1)
        head += "# Lon2: {:.6f}\n".format(lon2)

    # catch undefined queries
    else:
        raise ValueError("Undefined query type", qtype)

    return head

## Output function
#  - inputs: output dataframe, file path, query type
#  - returns: None
def write_csv_output(df, outfile, qtype, modelname):
    
    # write file without header
    df.to_csv(outfile, index=None, float_format="%.6f", na_rep=np.nan)

    # get header 
    qtext = get_csv_header(df, qtype, modelname)

    # update the file to include header
    with open(outfile, "r") as f:
        lines = f.readlines()
    with open(outfile, "w") as f:
        f.write(qtext)
        f.writelines(lines)   
