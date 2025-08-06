### Import Packages
import xarray as xr

## Initalize which dataset to choose from
# - inputs: Model name in string: 'Lee_2025' or 'Shinevar_2018'
# - outputs: file name of the inputs mode
def select_model(modelname):

    if modelname == 'Lee_2025':
        f_ctm = "./ThermalModel_WUS_v2.nc" 

    elif modelname == 'Shinevar_2018':
        f_ctm = "./Shinevar_2018_Temperature.nc" 

    return f_ctm

## initalize Xarray Dataset from netCDF file
#  - inputs: path to thermal model CDF
#  - returns: Xarray Dataset corresponding to the model
def init_ctm(modelname):
    
    # Get correct file name for inputs model name
    modelpath = select_model(modelname)
    
    # open dataset
    xdata = xr.open_dataset(modelpath)

    if modelname == 'Lee_2025':
        # configure: change unit to meters and rename all variables
        xdata = xdata.assign_coords({"depth": xdata.depth*1000.0})
        xdata = xdata.rename_dims({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]"})
        xdata = xdata.rename_vars({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]",
                                   "temperature_diffused": "temperature[°C]"})

    elif modelname == 'Shinevar_2018':
        # configure: rename all variables
        xdata = xdata.rename_dims({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]"})
        xdata = xdata.rename_vars({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]",
                                   "temperature": "temperature[°C]"})
        
    # return
    return xdata
