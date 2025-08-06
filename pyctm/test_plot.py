# Import packages
import matplotlib.pyplot as plt
import xarray as xr

## Plotting functions
#  - inputs: Xarray dataset to plot, query type (string)
#  - returns: figure handle
def test_plot(xdata, qtype):
    
    # plot a 2D vertical section 
    if qtype == "2D_vertical":
        fig = xdata["temperature[°C]"].plot(x="track index", y="depth[m]", yincrease=False,
            cbar_kwargs={"label": "Temperature [°C]"}, cmap="RdYlBu_r")

    # plot a 2D horizontal section
    elif qtype == "2D_horizontal":
        fig = xdata["temperature[°C]"].plot(cbar_kwargs={"label": "Temperature [°C]"}, cmap="RdYlBu_r")
    
    # plot a 1D vertical profile
    elif qtype == "1D_vertical":
        fig = xdata["temperature[°C]"].plot(y="depth[m]", yincrease=False)

    # undefined
    else:
        raise ValueError("Undefined plotting type", qtype)

    # return the Figure Handle
    return fig
