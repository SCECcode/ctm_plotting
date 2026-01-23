Instructions on how to run the Community Thermal Model (CTM) query Python (version 3.11.4) scripts
Daniel Trugman
Terry Lee
August 2025

Dependent packages requirement:
- matplotlib
- pandas
- numpy
- xarray
- pyproj

This package of Python scripts contains four query scripts to retrieve 0d points, 1d vertical depth profile, 2d cross section, and 2d horizontal slice.
These query scripts include:
- 'query_0d_point.py'
- 'query_1d_depth_profile.py'
- 'query_2d_cross_section.py'
- 'query_2d_horizontal_slice.py'


These query scripts has several dependent Python functions:
- 'Initation.py'
- 'Value_check.py'
- 'test_plot.py'
- 'calculate_geodesic_track.py'
- 'dTdz_2D_vertical_cross_section.py'
- 'write_csv_output.py'


Associated CTMs data from Lee et al. (2025) and Shinevar et al. (2018), as well as national models of Boyd (2019) and Sui et al. (2025) are also included here:
- 'ThermalModel_WUS_v2.nc'
- 'Shinevar_2018_Temperature.nc'
- 'NCM_TemperatureVolume_250929_ll.nc'
- 'Suietal_GJI_2025_vol.nc'


***Query_0d_point***
To run 'query_0d_point.py' script, at command prompt, go to the directory of all the scripts, then run "Python query_0d_point.py".
Command prompt will ask user to enter all the required input arguments:
- Latitude (°)
- Longitude (°)
- Depth (m)
- Model name: Either Lee_2025 or Shinevar_2018 or Boyd_2019 or Suietal_2025
- Input model path
- Output file path as .json file
Example:
Python query_0d_point.py --lat 40 --lon -115 --z 10000 --modelname 'Lee_2025' --modelpath 'ThermalModel_WUS_v2.nc' --outpath '0d_point_out.json'
Query 0d point returns a .json file.



***Query 1d depth profile***
To run 'query_1d_depth_profile.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_1d_depth_profile.py".
Command prompt will ask user to enter all the required input arguments:
- Latitude (°)
- Longitude (°)
- Starting depth (m)
- Ending depth (m)
- Depth interval (m)
- Model name: Either Lee_2025 or Shinevar_2018 or Boyd_2019 or Suietal_2025
Example:
Python query_1d_depth_profile.py --lat 40 --lon -115 --z_start 0 --z_end 20000 --z_step 1000 --modelname 'Lee_2025' --modelpath 'ThermalModel_WUS_v2.nc' --outpath 'test1d.csv'
Query 1d depth profile returns a .csv file.



***Query 2d cross section***
To run 'query_2d_cross_section.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_2d_cross_section.py".
Command prompt will ask user to enter all the required input arguments:
- Starting latitude (°)
- Starting longitude (°)
- Ending latitude (°)
- Ending longitude (°)
- Starting depth (m)
- Ending depth (m)
- Model name: Either Lee_2025 or Shinevar_2018 or Boyd_2019 or Suietal_2025
Example:
Python query_2d_cross_section.py --lat_start 40 --lon_start -115 --lat_end 42 --lon_end -113 --z_start 0 --z_end 20000 --modelname 'Lee_2025' --modelpath 'ThermalModel_WUS_v2.nc' --outpath 'test2d_cross.csv'
Query 2d cross section returns a .csv file.



***Query 2d horizontal slice***
To run 'query_2d_horizontal_slice.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_2d_horizontal_slice.py".
Command prompt will ask user to enter all the required input arguments:
- Starting latitude (°)
- Starting longitude (°)
- Ending latitude (°)
- Ending longitude (°)
- Depth (m)
- Model name: Either Lee_2025 or Shinevar_2018 or Boyd_2019 or Suietal_2025
Example:
Python query_2d_horizontal_slice.py --lat_start 40 --lon_start -115 --lat_end 42 --lon_end -113 --z 10000 --modelname 'Lee_2025' --modelpath 'ThermalModel_WUS_v2.nc' --outpath 'test2d_horizontal.csv'
Query 2d horizontal slice returns a .csv file.
