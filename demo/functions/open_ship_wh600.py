"""
This tests all ship_wh600 files specified in ../paths.xlsx
"""

import os
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

import themachinethatgoesping as theping
from themachinethatgoesping import pingprocessing as pp


paths_key = "SHIP_WH600"

SHIP_WH600_KEYS = [
    "DateTime",
    #"BottomRange",
    "Heading",
    "Lat",
    "Lon",
    "bin1",
]

SHIP_WH600_KEYS_alt = [
    "DateTime",
    #"BottomRange",
    "Heading",
    "Lat",
    "Lon",
    "bin 1",
]

OUT_KEYS = [
    "Unixtime",
    "Datetime",
    "MDates",
    #"Depth_m",
    #"Bottomrange_m",
    "Heading_deg",
    "Latitude",
    "Longitude",
    "data",
    "nbins",
]


def get_datetime(data):
    """Converts the time columns to datetime"""
    datetime = pd.to_datetime(data["DateTime"], utc=True, dayfirst=True)
    return datetime

def data_to_echogramdata(data, bin_size=0.25, depth_offset=5.8+1.3):
    """Converts the data to an echogram section"""
    im, extent = data_to_image(data, bin_size=bin_size, depth_offset=depth_offset)

    echodata = theping.pingprocessing.watercolumn.echograms.EchoData(im, data["Unixtime"].values)

    min_range = np.empty(im.shape[0])
    max_range = np.empty(im.shape[0])
    min_range.fill(bin_size*0.5)
    max_range.fill(bin_size*(0.5+im.shape[1]))
    echodata.set_range_extent(min_range, max_range)
    echodata.set_depth_extent(min_range + depth_offset, max_range + depth_offset)

    echodata.add_ping_param("echosounder", "Ping time", "Depth (m)", data["Unixtime"].values, [depth_offset for _ in data["Unixtime"].values])

    return echodata

def data_to_image(data, bin_size=0.25, depth_offset=5.8):
    im = np.empty((len(data), np.nanmax(data["nbins"])))
    im.fill(np.nan)
    for i in range(len(data)):
        im[i, : data["nbins"][i]] = data["data"][i]

    # get delta time
    data["delta_time"] = data["Unixtime"].shift(-1) - data["Unixtime"]
    delta_time = np.nanmedian(data["delta_time"].values)

    extent = [
        (data["Datetime"][0] - pd.Timedelta(delta_time / 2, unit="s")).to_pydatetime(),
        (data["Datetime"].iat[-1] + pd.Timedelta(delta_time / 2, unit="s")).to_pydatetime(),
        bin_size * im.shape[1] - bin_size / 2 + depth_offset,
        bin_size / 2 + depth_offset,
    ]

    return im, extent


def open_ship_wh600(path):
    """Open ship_wh600 data
    The data is assumed to be xlsx format
    It must contain exactly the keys specified in SHIP_WH600_KEYS or SHIP_WH600_KEYS_alt

    Parameters
    ----------
    path : str
        Path to the data file, path must be relative to the data directory

    Returns
    -------
    pandas.DataFrame
        pandas dataframe containing the data
        + unixtime, datetime
    """

    data_in = pd.read_csv(path)

    assert all(k in list(data_in.keys()) for k in SHIP_WH600_KEYS) or all(k in list(data_in.keys()) for k in SHIP_WH600_KEYS_alt), f"Keys for {path} are not correct"

    # get data columns
    data = pd.DataFrame()
    datetime = get_datetime(data_in)
    data["Unixtime"] = datetime.map(pd.Timestamp.timestamp)
    data["Datetime"] = datetime
    data["MDates"] = mdates.date2num(data["Datetime"])
    #data["Depth_m"] = data_in["BottomRange"] + 5.8
    #data["Bottomrange_m"] = data_in["BottomRange"]
    data["Heading_deg"] = data_in["Heading"]
    data["Latitude"] = data_in["Lat"]
    data["Longitude"] = data_in["Lon"]

    # get data
    data_keys = [key for key in data_in.keys() if key.startswith("bin")]
    # data_keys.sort()
    data["data"] = data_in[data_keys].values.tolist()
    data["nbins"] = len(data_keys)

    # remove duplicate rows
    data.drop_duplicates(subset="Unixtime", inplace=True)

    # filter out bad data

    # sort by time
    data.sort_values(by=["Unixtime"], inplace=True)

    # reset index
    data.reset_index(drop=True, inplace=True)

    # test that all columns are present
    assert list(data.keys()) == list(OUT_KEYS), f"Keys for {path} are not correct"

    return data
