"""
  @file setup.py
  @brief Build and install the pyctm
  @author The SCEC/CTM Developers - <software@scec.usc.edu>

"""

from setuptools import setup


NAME = "ctm_plotting"
FULLNAME = "ctm_plotting with pyctm"
AUTHOR = "The SCEC/CTM Developers"
AUTHOR_EMAIL = "software@scec.usc.edu"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "Apache 2.0 license"
URL = "https://github.com/SCECcode/ctm_plotting"
DESCRIPTION = "Python code extensions for CTM and plotting library for the SCEC CTM"

with open("README.md") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

VERSION = "0.0.2"

CLASSIFIERS = [
    "Development Status :: 1 - Alpha",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.11.0",
    "License :: OSI Approved :: {}".format(LICENSE),
]
PLATFORMS = "Any"
INSTALL_REQUIRES = ["numpy", "matplotlib", "pandas", "xarray", "pyproj",  "packaging"]
KEYWORDS = ["CTM"]

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        packages=["pyctm"], 
        scripts=[ "ctm_plotting/query_0d_point.py", "ctm_plotting/query_1d_depth_profile.py",
                  "ctm_plotting/query_2d_cross_section.py", "ctm_plotting/query_2d_horizontal_slice.py" ] 
    )
