# Import package
import numpy as np
from pyproj import Geod

## Calculate a geodesic track between lon, lat pairs
#  - inputs: start longitude and latitude, end longitude and latitude, number of points
#  - returns: longitude and latitude arrays along this track
def calculate_geodesic_track(lonA, latA, lonB, latB, npts):
    
    # define ellipse for geodesic
    g = Geod(ellps="WGS84")

    # sample points along geodesic (including start and end points)
    pts = g.npts(lonA, latA, lonB, latB, npts, initial_idx=0, terminus_idx=0)
    
    # extract arrays
    glons = np.array([x[0] for x in pts])
    glats = np.array([x[1] for x in pts])

    # return
    return glons, glats
