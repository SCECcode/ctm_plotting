# Import package
import pandas as pd

##  Calculate geothermal gradient for a 2D vertical slice
# - input: Dataframe output from query_2D_vertical_cross_section()
# - returns: Dataframe with geothermal gradient, latitude, and longitude
def dTdz_2D_vertical_cross_section(df):
    
    df_copy = df.copy()                                                    # Make a copy of the queried dataframe
    df_copy['lonlat'] = list(zip(df['Lon'], df['Lat']))   # Make a new column to store longitude and latitude together

    grouped = df_copy.groupby(['lonlat'])         # Group data by lonlat tuple
    dTdz_dic = []                                 # Make an empty list to store results later
    
    # Loop through each profile to calculate linear dTdz
    for lonlat, group in grouped:
        group = group.sort_values('Depth(m)')      # Sort each group df by depth
        z_min = group['Depth(m)'].iloc[0]          # Find minimum depth
        z_max = group['Depth(m)'].iloc[-1]         # Find maximum depth
        T_min = group['Temperature(°C)'].iloc[0]   # Find minimum temperature
        T_max = group['Temperature(°C)'].iloc[-1]  # Find maximum temperature
        
        dTdz = ((T_max - T_min) / (z_max - z_min)) * 1000  # Calculate geothermal gradient, °C/km

        # Store result to the dictionary
        dTdz_dic.append({
            'longitude[°]': lonlat[0][0],
            'latitude[°]': lonlat[0][1],
            'dTdz[°C/km]': dTdz})

        # Convert dictionary to dataframe
        df_dTdz = pd.DataFrame(dTdz_dic)

    return df_dTdz
