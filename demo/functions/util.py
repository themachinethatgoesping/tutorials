import xarray as xr
import pandas as pd
import datetime

def image_to_xarray(
    image, 
    extent,
    name=None,
    xdim='x',
    ydim='y',
    **attrs
):
    xres = (extent[1]-extent[0])/(image.shape[0])
    yres = (extent[3]-extent[2])/(image.shape[1])

    x_coords = [extent[0]-xres/2 +xres*x for x in range(image.shape[0])]
    y_coords = [extent[2]-yres/2 +yres*y for y in range(image.shape[1])]
    
    if isinstance(x_coords[0],datetime.datetime):
        x_coords = pd.to_datetime(x_coords).tz_localize(None)
    
    # Convert to xarray DataArray
    da = xr.DataArray(
        image,
        name=name,
        dims=[xdim, ydim],
        coords={xdim: x_coords, ydim: list(reversed(y_coords))},
        attrs=attrs,
    )

    return da