import numpy as np
import importlib.metadata

# __version__ = importlib.metadata.version("airpollutionwatch")


def wdws2wxwy(wdws):
    """wd: direction that wind comes from"""
    direc, speed = wdws[:, 0], wdws[:, 1]
    theta = direc * np.pi / 8  # verified with convert_wind.py
    return speed * np.c_[np.sin(theta), np.cos(theta)]
