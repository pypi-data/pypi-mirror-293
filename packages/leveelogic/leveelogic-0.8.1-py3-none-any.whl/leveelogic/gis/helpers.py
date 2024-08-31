from pyproj import Transformer
from typing import Tuple


def xy_to_latlon(x: float, y: float, epsg: int = 28992) -> Tuple[float, float]:
    """Convert coordinates from the given epsg to latitude longitude coordinate

    Arguments:
        x (float): x coordinate
        y (float): y coordinate
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         Tuple[float, float]: latitude, longitude rounded to 6 decimals
    """
    if epsg == 4326:
        return x, y

    try:
        transformer = Transformer.from_crs(epsg, 4326)
        lat, lon = transformer.transform(x, y)
    except Exception as e:
        raise e

    return (round(lat, 6), round(lon, 6))


def latlon_to_xy(lat: float, lon: float, epsg=28992) -> Tuple[float, float]:
    """Convert latitude longitude coordinate to given epsg

    Arguments:
        lat (float): latitude
        lon (float): longitude
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         Tuple[float, float]: x, y in given epsg coordinate system
    """
    try:
        transformer = Transformer.from_crs(4326, epsg)
        x, y = transformer.transform(lat, lon)
    except Exception as e:
        raise e

    return (x, y)
