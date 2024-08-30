# -*- coding: UTF-8 -*-
"""
@Name:_polygon_to_grid.py
@Auth:yujw
@Date:2024/8/22-上午11:27
"""
import chardet
import geopandas as gpd
from pathlib import Path

import numpy as np
from shapely import MultiLineString, Polygon, MultiPolygon
from skimage import measure
import xarray as xr
import re

from wz_core_points_utils.diamond14 import Diamond14

p_s = re.compile('\\s+')


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read(248))['encoding']


def __get_polygons(geometries, f_number=4):
    """
    规则统一，全部转成polygon类型
    :param geometries:
    :param f_number:
    :return:
    """
    polys = []
    for geo1 in geometries:
        if isinstance(geo1, MultiLineString):
            for geo in list(geo1.geoms):
                poly = [(xx, yy) for xx, yy in zip(geo.xy[0], geo.xy[1])]
                if len(poly) < f_number:
                    continue
                polys.append(Polygon(poly))
            # polys.append(MultiPolygon(polygons))
        elif isinstance(geo1, MultiPolygon):
            polys.extend(__get_polygons([geo1.boundary], f_number))
        elif isinstance(geo1, Polygon):
            boy = geo1.boundary
            if isinstance(boy, MultiLineString):
                polygons = []
                for geo in list(boy.geoms):
                    poly = [(xx, yy) for xx, yy in zip(geo.xy[0], geo.xy[1])]
                    if len(poly) < f_number:
                        continue
                    polygons.append(Polygon(poly))
                polys.append(MultiPolygon(polygons))
            else:
                poly = [(xx, yy) for xx, yy in zip(geo1.boundary.xy[0], geo1.boundary.xy[1])]
                if len(poly) < f_number:
                    continue
                polys.append(Polygon(poly))
        else:
            xy = geo1.xy
            poly = [(xx, yy) for xx, yy in zip(xy[0], xy[1])]
            if len(poly) < f_number:
                continue
            polys.append(Polygon(poly))

    return polys


def read_area_file(file_path: str, default_value=10):
    """
    读取落区文件
    :param default_value:
    :param file_path:文件路径
    :return:
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"{file_path} not exists!!!")
    if file_path.endswith(".shp") or file_path.endswith(".geojson") or file_path.endswith(".json"):
        gpd_data = gpd.read_file(file_path)
        return __get_polygons(gpd_data.geometry.values), [default_value] * len(gpd_data)
    dia = Diamond14(file_path)
    gpd_data = dia.open()
    return __get_polygons(gpd_data.geometry.values), gpd_data["value"].values
    # return __read_diamond14_file(file_path)


def polygon_to_grid(polygons, polygon_values, lat1, lat2, lon1, lon2, dx, dy, fill_value=9999,
                    dtype=np.float32) -> xr.DataArray:
    """
    将线条转成 二维场
    :param dtype:
    :param polygon_values:
    :param fill_value:
    :param polygons:
    :param lat1:
    :param lat2:
    :param lon1:
    :param lon2:
    :param dx:
    :param dy:
    :return:
    """
    if len(polygon_values) != len(polygons):
        raise Exception("polygon_values 与 polygons 长度不一致")
    latitudes = np.arange(lat1, lat2 + dy, dy)
    longitudes = np.arange(lon1, lon2 + dx, dx)
    final_values = np.full((len(latitudes), len(longitudes)), fill_value, dtype=dtype)
    for pol, val in zip(polygons, polygon_values):
        longitude, latitude = pol.exterior.coords.xy
        z_ = np.empty((len(latitude), 2))
        lat_idx = ((np.array(latitude) - lat1) / dy).astype(int)
        lon_idx = ((np.array(longitude) - lon1) / dx).astype(int)
        z_[:, 0] = lat_idx
        z_[:, 1] = lon_idx
        d_tmp = measure.grid_points_in_poly((len(latitudes), len(longitudes)), z_)
        final_values = np.where(d_tmp, val, final_values)

    xr_data = xr.DataArray(final_values, coords=[('lat', latitudes), ('lon', longitudes)], name='data0',
                           attrs={"lat1": lat1, "lat2": lat2, "lon1": lon1, "lon2": lon2, "dx": dx, "dy": dy,
                                  "fill_value": fill_value, "nx": len(longitudes), "ny": len(latitudes)})
    return xr_data
