from typing import List, Tuple
from shapely.geometry import (
    LineString,
    MultiPoint,
    Point,
    GeometryCollection,
    MultiLineString,
)
from shapely import get_coordinates
import math
from pathlib import Path


def case_insensitive_glob(filepath: str, fileextension: str) -> List[Path]:
    """Find files in given path with given file extension (case insensitive)

    Arguments:
        filepath (str): path to files
        fileextension (str): file extension to use as a filter (example .gef or .csv)

    Returns:
        List(str): list of files
    """
    p = Path(filepath)
    result = []
    for filename in p.glob("**/*"):
        if str(filename.suffix).lower() == fileextension.lower():
            result.append(filename.absolute())
    return result


def polyline_polyline_intersections(
    points_line1: List[Tuple[float, float]],
    points_line2: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    result = []
    ls1 = LineString(points_line1)
    ls2 = LineString(points_line2)
    intersections = ls1.intersection(ls2)

    if intersections.is_empty:
        return []
    elif type(intersections) == MultiPoint:
        result = [(g.x, g.y) for g in intersections.geoms]
    elif type(intersections) == Point:
        x, y = intersections.coords.xy
        result = [(x[0], y[0])]
    elif type(intersections) == LineString:
        result += [(p[0], p[1]) for p in get_coordinates(intersections).tolist()]
    elif type(intersections) == GeometryCollection:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        result += [(p[0], p[1]) for p in get_coordinates(geoms).tolist()]
        for p in [g for g in intersections.geoms if type(g) == Point]:
            x, y = p.coords.xy
            result.append((x[0], y[0]))
    elif type(intersections) == MultiLineString:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        if len(geoms) >= 2:
            x1, z1 = geoms[0].coords.xy
            x2, z2 = geoms[1].coords.xy

            if x1 == x2:  # vertical
                x = x1.tolist()[0]
                zs = z1.tolist() + z2.tolist()
                result.append((x, min(zs)))
                result.append((x, max(zs)))
            elif z1 == z2:  # horizontal
                z = z1.tolist()[0]
                xs = x1.tolist() + x2.tolist()
                result.append((min(xs), z))
                result.append((max(xs), z))
            else:
                raise ValueError(
                    f"Unimplemented intersection type '{type(intersections)}' that is not a horizontal or vertical line or consists of more than 2 lines"
                )
        else:
            raise ValueError(
                f"Unimplemented intersection type '{type(intersections)}' with varying x or z coordinates"
            )
    else:
        raise ValueError(
            f"Unimplemented intersection type '{type(intersections)}' {points_line1}"
        )

    # do not include points that are on line1 or line2
    # final_result = [float(p) for p in result if not p in points_line1 or p in points_line2]

    # if len(final_result) == 0:
    #    return []

    return sorted(result, key=lambda x: x[0])


def is_on_line(point_a, point_b, point_c, tolerance=1e-6):
    """
    This function checks if point_c lies on the line formed by point_a and point_b,
    considering a tolerance for floating-point errors and handling vertical lines.

    Args:
    point_a: A tuple of two floats (x, y) representing coordinates.
    point_b: A tuple of two floats (x, y) representing coordinates.
    point_c: A tuple of two floats (x, y) representing coordinates.
    tolerance: A small value to account for floating-point errors (default: 1e-6).

    Returns:
    True if point_c is on the line within the tolerance, False otherwise.
    """
    # Check for collinearity (all three points are aligned)
    if point_c[0] <= min(point_a[0], point_b[0]):
        return False
    if point_c[0] >= max(point_a[0], point_b[0]):
        return False
    if point_c[1] <= min(point_a[1], point_b[1]):
        return False
    if point_c[1] >= max(point_a[1], point_b[1]):
        return False

    if point_a[0] == point_b[0] and point_a[0] == point_c[0]:
        return True
    if point_a[1] == point_b[1] and point_a[1] == point_c[1]:
        return True

    # Handle the case of a vertical line (where x-coordinates of A and B are the same)
    if abs(point_a[0] - point_b[0]) <= tolerance:
        return abs(point_c[0] - point_a[0]) <= tolerance
    else:
        # Calculate the slope and check if C's y-coordinate is within tolerance of the line equation
        slope = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        return (
            abs(point_c[1] - (slope * (point_c[0] - point_a[0]) + point_a[1]))
            <= tolerance
        )


def is_part_of_line(point_a, point_b, point_c, tolerance=1e-6) -> bool:
    """Check if point c is either a or b

    Args:
        point_a (_type_): A tuple of two floats (x, y) representing coordinates
        point_b (_type_): A tuple of two floats (x, y) representing coordinates
        point_c (_type_): A tuple of two floats (x, y) representing coordinates
        tolerance (_type_, optional): A small value to account for floating-point errors. Defaults to 1e-6.

    Returns:
        bool: True is point c is point a or point b (within the given tolerance)
    """
    dLA = math.hypot(point_a[0] - point_c[0], point_a[1] - point_c[1])
    dLB = math.hypot(point_b[0] - point_c[0], point_b[1] - point_c[1])
    return dLA <= tolerance or dLB <= tolerance
