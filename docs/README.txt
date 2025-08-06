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

Associated CTMs data from Lee et al. (2025) and Shinevar et al. (2018) are also included here:
- 'ThermalModel_WUS_v2.nc'
- 'Shinevar_2018_Temperature.nc'



***Query_0d_point***
To run 'query_0d_point.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_0d_point.py".
Command prompt will ask user to enter all the required input arguments:
- Latitude (°)
- Longitude (°)
- Depth (m)
- Model name: Either Lee_2025 or Shinevar_2018
Query 0d point does not returns any output files. Instead, the query results will be printed.



***Query 1d depth profile***
To run 'query_1d_depth_profile.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_1d_depth_profile.py".
Command prompt will ask user to enter all the required input arguments:
- Latitude (°)
- Longitude (°)
- Starting depth (m)
- Ending depth (m)
- Depth interval (m)
- Model name: Either Lee_2025 or Shinevar_2018
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
- Model name: Either Lee_2025 or Shinevar_2018
Query 2d cross section returns a .csv file.



***Query 2d horizontal slice***
To run 'query_2d_horizontal_slice.py' script, at command prompt, go to the directory of all of scripts, then run "Python query_2d_horizontal_slice.py".
Command prompt will ask user to enter all the required input arguments:
- Starting latitude (°)
- Starting longitude (°)
- Ending latitude (°)
- Ending longitude (°)
- Depth (m)
- Model name: Either Lee_2025 or Shinevar_2018
Query 2d horizontal slice returns a .csv file.