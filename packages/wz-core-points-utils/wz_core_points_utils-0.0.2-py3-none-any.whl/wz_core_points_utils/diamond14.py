# -*- coding: UTF-8 -*-
"""
@Name:diamond14.py
@Auth:yujw
@Date:2023/12/14-9:33
"""
import chardet
import numpy as np

import re
from shapely.geometry.linestring import LineString
from shapely import Point, Polygon

comp = re.compile("\\s+")


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read(248))['encoding']


class Diamond14:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path, "r", encoding=get_encoding(file_path)) as f:
            self.lines = f.readlines()
            self.lines = [line.strip() for line in self.lines if len(line.strip()) > 0]
        self.geometries = []
        self.labels = []
        self.values = []
        self.names = []
        self.number = 4
        self.point_type = {
            24: "雨雪",
            26: "小雨",
            47: "中雨",
            55: "大雨",
            64: "暴雨",
            221: "大暴雨",
            231: "特大暴雨",
            23: "小雪",
            22: "中雪",
            21: "大雪",
            66: "暴雪",
            70: "霾",
            201: "浮尘",
            45: "扬沙",
            211: "沙暴",
            46: "轻沙暴",
            29: "轻雾",
            30: "雾",
            157: "臭氧",
        }

    def __filter_get_index(self, title):
        for idx, line in enumerate(self.lines):
            if line.startswith(title):
                return idx
        return None

    def open_lines(self):
        title = "LINES"
        _index = self.__filter_get_index(title)
        number = int(self.lines[_index].split(":")[1])
        if number != 0:
            pass

    def __get_indexes(self, title, data_interval=2):
        _index = self.__filter_get_index(title)
        number = int(self.lines[_index].split(":")[1])
        if number == 0:
            return
        # 计算下标
        list_index = []
        for idx in range(number):
            detail = comp.split(self.lines[int(_index + 1)].strip())

            if len(detail) == 3:
                count = int(detail[2])
                col_len = int(detail[1])
                mod = count % col_len
                self.number = int(detail[1])
            elif len(detail) == 2:
                count = int(detail[1])
                mod = int(detail[1]) % self.number

            rows = (count - mod) / self.number
            rows = rows if mod == 0 else rows + 1
            list_index.append([int(_index + data_interval), int(_index + data_interval - 1 + rows)])
            _index = _index + data_interval + rows

        return list_index

    def open_lines_symbol(self):
        title = "LINES_SYMBOL"

        list_index = self.__get_indexes(title)
        if list_index is None:
            return
        for indexes in list_index:
            start_index, end_index = indexes[0], indexes[1]
            line_arr = []
            [line_arr.extend(comp.split(self.lines[index].strip())) for index in range(start_index, end_index + 1)]
            np_arr = np.array(line_arr, dtype=float).reshape((int(len(line_arr) / 3), 3))
            linestring = LineString([[arr[0], arr[1]] for arr in np_arr])
            self.labels.append(title)
            self.names.append("")
            self.geometries.append(linestring)
            self.values.append(9999)

    def open_symbols(self):
        title = "SYMBOLS"
        _index = self.__filter_get_index(title)
        number = int(self.lines[_index].split(":")[1])
        if number == 0:
            return
        start_index = _index + 1
        end_index = start_index + number
        lamb_func = lambda index: comp.split(self.lines[index].strip())
        points = [Point(float(lin_arr[1]), float(lin_arr[2])) for lin_arr in
                  list(map(lamb_func, range(start_index, end_index)))]
        self.geometries.extend(points)
        self.labels.extend([title] * len(points))
        self.names.extend(
            [self.point_type[int(lin_arr[0])] for lin_arr in list(map(lamb_func, range(start_index, end_index)))])
        self.values.extend([int(lin_arr[0]) for lin_arr in list(map(lamb_func, range(start_index, end_index)))])

    def open_closed_contours(self):
        title = "CLOSED_CONTOURS"
        list_index = self.__get_indexes(title, data_interval=3)
        if list_index is None:
            return
        for indexes in list_index:
            start_index, end_index = indexes[0], indexes[1]
            line_arr = []
            [line_arr.extend(comp.split(self.lines[index].strip())) for index in range(start_index - 1, end_index)]
            np_arr = np.array(line_arr, dtype=float).reshape((int(len(line_arr) / 3), 3))

            linestring = Polygon([[arr[0], arr[1]] for arr in np_arr])
            self.labels.append(title)
            self.geometries.append(linestring)
            self.names.append("")
            self.values.append(float(comp.split(self.lines[end_index].strip())[0]))

    def open_station_situation(self):
        pass

    def open_weather_region(self):
        pass

    def open_fill_area(self):
        pass

    def open_notes_symbol(self):
        pass

    def open(self):
        import geopandas as gpd
        from cartopy import crs

        self.open_lines_symbol()
        self.open_closed_contours()
        self.open_symbols()
        gpd_data = gpd.GeoDataFrame(
            {"geometry": self.geometries, "label": self.labels, "name": self.names, "value": self.values},
            crs=crs.PlateCarree())
        return gpd_data
