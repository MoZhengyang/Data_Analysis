# this module is mainly used to write the algorithm
import numpy as np
from math import radians, sin, cos, asin, sqrt
from pykrige import OrdinaryKriging
import fiona
from shapely.geometry import Polygon as Poly
from shapely.geometry import MultiPolygon
from geojson import Polygon, Feature, FeatureCollection
from geopandas import GeoDataFrame


def caldis(lon1, lat1, lon2, lat2):
    # 计算两点之间距离，经纬度坐标距离与真实距离转换
    a = radians(lat1-lat2)
    b = radians(lon1 - lon2)
    lat1, lat2 = radians(lat1), radians(lat2)
    t = sin(a/2)**2 + cos(lat1)*cos(lat2)*sin(b/2)**2
    d = 2*asin(sqrt(t))*6378.137
    return d


# 由宿迁市shp地理数据  /必须包括dbf，shp，shx文件
# 确定宿迁市经纬度
class Krg:
    def __init__(self):

        self.pos = None
        self.lon_min = 0
        self.lon_max = 0
        self.lat_min = 0
        self.lat_max = 0
        self.dpi = 0

    def boundary(self, shp_path):
        # 对shp数据解析获得经纬度边界
        shp = fiona.open(shp_path)
        pos = next(iter(shp))['geometry']['coordinates'][0]
        lons = [lon for (lon, _) in pos]
        lats = [lat for _, lat in pos]
        self.lon_min, self.lon_max = min(lons), max(lons)
        self.lat_min, self.lat_max = min(lats), max(lats)
        self.pos = pos  # 保存pos的信息，krg函数调用
        return lons, lats

    def krg(self, lon_norm, lat_norm, tm_norm, step=135, conduce_data_name="temperature"):
        # 生成区域网格
        grid_lon = np.linspace(self.lon_min-0.1, self.lon_max+0.1, step)
        s_lon = grid_lon[1] - grid_lon[0]
        grid_lat = np.linspace(self.lat_min - 0.1, self.lat_max + 0.1, step)
        s_lat = grid_lat[1] - grid_lat[0]
        # krige 插值
        print(conduce_data_name)
        if max(tm_norm) == min(tm_norm):
            tm_norm[0] += 0.001
        ordkrige = OrdinaryKriging(lon_norm, lat_norm, tm_norm, variogram_model='gaussian', nlags=6)
        zgrid, _ = ordkrige.execute('grid', grid_lon, grid_lat)
        xgrid, ygrid = np.meshgrid(grid_lon, grid_lat)
        x, y, z = xgrid.flatten(), ygrid.flatten(), zgrid.flatten()
        # 获得相邻两点之间的距离
        self.dpi = caldis(x[0], y[0], x[1], y[1])
        # 获得区域每个网格的坐标表示与对应的温度，存储在list中
        # 宿迁市行政区多边形
        area_poly = Poly(self.pos)
        positions, temps = self.atv(x, y, z, s_lon, s_lat, area_poly)
        # 数据转换成GeoDataFrame，便于folium调用画图
        tempgdf = self.togdf(positions, temps, conduce_data_name)
        return tempgdf

    def togdf(self, positions, temps, conduce_data_name):
        features = []
        color = []
        k = 1
        for position, tem in zip(positions, temps):
            polygon = Polygon(position)
            features.append(Feature(geometry=polygon, properties={"area": k}))
            color.append([k, tem])
            k += 1
        feature_collection = FeatureCollection(features)
        temp = GeoDataFrame.from_features(feature_collection, crs="epsg:4326")
        unit = {"temperature": "℃", "pressure": "hPa", "humidity": "%RH", "speed": "m/s", "rainfall": "mm/min",
                "total_radiation": "W/m²", "radiation_all": "MJ/m²", "rainfall_all": "mm", "illumination": "LUX"}
        temp[conduce_data_name] = np.array(color)[:, 1]
        temp[conduce_data_name+'_str'] = [str(round(x, 1)) + unit[conduce_data_name] for _, x in color]
        return temp

    def atv(self, x, y, z, s_lon, s_lat, poly):
        positions = []
        temps = []
        for lon, lat, tem in zip(x, y, z):
            # 每个坐标对应的小方格
            rectangle = Poly([(lon - s_lon / 2, lat + s_lat / 2), (lon + s_lon / 2, lat + s_lat / 2),
                          (lon + s_lon / 2, lat - s_lat / 2), (lon - s_lon / 2, lat - s_lat / 2),
                          (lon - s_lon / 2, lat + s_lat / 2)])
            intersec = poly.intersection(rectangle)
            if not intersec.is_empty:
                if type(intersec) is MultiPolygon:
                    for i in range(len(intersec.geoms)):
                        positions.append([[[lon, lat] for lon, lat in list(intersec.geoms[i].exterior.coords)]])
                        temps.append(tem)
                else:
                    positions.append([[[lon, lat] for lon, lat in list(intersec.exterior.coords)]])
                    temps.append(tem)
        return positions, temps



















