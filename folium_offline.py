
import os
import folium
import nhzn_krige
from jinja2 import Template
from pandas import read_csv as rcsv
from pandas import read_excel as rexcel

import json
import os
from utils import *
# 对应自己的python包的安装地址
# os.environ['PROJ_LIB'] = r'D:\Anaconda\envs\NHZN\Library\share\proj'
# os.environ['GDAL_DATA'] = r'D:\Anaconda\envs\NHZN\Library\share\gdal'


def add_marker(map, vate_temple, site_lon, site_lat, site_temp, site_name, temp_norm_index, conduce_data_name, unit, hist_data):
    # 获得sites对应的历史温度信息，并依据此建立vetalite的temple
    for name, lon, lat, temp, normal in zip(site_name, site_lon, site_lat, site_temp, temp_norm_index):
        # 得到修改后的模板
        temple = modify_temple(conduce_data_name, unit, vate_temple, name, hist_data)
        # 添加marker
        if normal:
            html = '<div style="font-size:10pt;font-weight:bold"><font color="green">{name}</font>:<font color="green">{temp}{unit}</font> </div>'.format(
                name=name, temp=round(temp, 1), unit=unit[conduce_data_name])
            tooltip = folium.Tooltip(html)
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup().add_child(folium.VegaLite(temple, width=450, height=250)),
                icon=folium.Icon(color='green'),
                tooltip=tooltip
            ).add_to(map)

        else:
            html = '<div style="font-size:10pt;font-weight:bold"><font color="red">{name}</font>:<font color="red">{temp}{unit}</font> </div>'.format(
                name=name, temp=round(temp, 1), unit=unit[conduce_data_name])
            tooltip = folium.Tooltip(html)
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup().add_child(folium.VegaLite(temple, width=450, height=250)),
                icon=folium.Icon(color='red'),
                tooltip=tooltip
            ).add_to(map)
        '''
        # 添加marker对应的文字显示
        if normal:
            folium.Marker(
                location=[lat, lon-0.00025],
                icon=folium.DivIcon(
                    icon_size=(20, 1),
                    icon_anchor=(0, 0),
                    html='<div style="font-size:14pt;font-weight:bold"><font color="#2987ce">{name}</font>:<font color="#2987ce">{temp}{unit}</font> </div>'.format(
                        name=name, temp=round(temp, 1), unit=unit[conduce_data_name])
                )
            ).add_to(map)
        else:
            folium.Marker(
                location=[lat, lon - 0.00025],
                icon=folium.DivIcon(
                    icon_size=(200, 10),
                    icon_anchor=(0, 0),
                    html='<div style="font-size:14pt;font-weight:bold"><font color="#2987ce">{name}</font>:<font color="red">{temp}{unit}</font> </div>'.format(
                        name=name, temp=round(temp, 1), unit=unit[conduce_data_name])
                )
            ).add_to(map)
            '''
    return map

def set_offline(file_path):
    """
    Change folium Map templating to look for required .js and .css locally.
    NOTE: These versions may change in time. You must manage/update them manually.
    :param file_path: str system file path to offline file directory
    :return: None
    """
    # compare to _default_js[...] in folium.py
    # modified to look for required .js in ./offline/
    # change relative path to your offline files
    folium.folium.Map.default_js = [
        ('leaflet',
         f'{os.path.join(file_path, "leaflet.js")}'),
        ('jquery',
         f'{os.path.join(file_path, "jquery-1.12.4.min.js")}'),
        ('bootstrap',
         f'{os.path.join(file_path, "bootstrap.min.js")}'),
        ('awesome_markers',
         f'{os.path.join(file_path, "leaflet.awesome-markers.js")}'),
        ('sql',
         f'{os.path.join(file_path, "sql.js")}'),
        ('sql-wasm',
         f'{os.path.join(file_path, "sql-wasm.js")}'),
        ('sql-asm',
         f'{os.path.join(file_path, "sql-asm.js")}'),
        ('mbtiles',
         f'{os.path.join(file_path, "Leaflet.TileLayer.MBTiles.js")}')
    ]

    # compare to _default_css[...] in folium.py
    # modified to look for required .css in ./offline/
    # change relative path to your offline files
    folium.folium.Map.default_css = [
        ('leaflet_css',
         f'{os.path.join(file_path, "leaflet.css")}'),
        ('bootstrap_css',
         f'{os.path.join(file_path, "bootstrap.min.css")}'),
        ('bootstrap_theme_css',
         f'{os.path.join(file_path, "bootstrap-theme.min.css")}'),
        ('awesome_markers_font_css',
         f'{os.path.join(file_path, "font-awesome.min.css")}'),
        ('awesome_markers_css',
         f'{os.path.join(file_path, "leaflet.awesome-markers.css")}'),
        ('awesome_rotate_css',
         f'{os.path.join(file_path, "leaflet.awesome.rotate.css")}')
    ]


def set_online(file_path):
    """
    Change folium Map templating to include Leaflet.TileLayer.MBTiles.js (offline file) and sql.js.
    :return: None
    """

    folium.folium.Map.default_js = [
        ('leaflet',
         'https://cdn.jsdelivr.net/npm/leaflet@1.5.1/dist/leaflet.js'),
        ('jquery',
         'https://code.jquery.com/jquery-1.12.4.min.js'),
        ('bootstrap',
         'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
        ('awesome_markers',
         'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js'),
        ('sql',
         'https://unpkg.com/sql.js@0.3.2/js/sql.js'),
        ('mbtiles',
         f'{os.path.join(file_path, "Leaflet.TileLayer.MBTiles.js")}')
    ]


def set_mbtiles():
    """
    Change folium TileLayer templating from L.tileLayer to L.tileLayer.mbTiles
    Uses Leaflet.TileLayer.MBTiles.js
    https://gitlab.com/IvanSanchez/Leaflet.TileLayer.MBTiles
    :return: None
    """

    # compare to folium raster_layers TileLayer _template in raster_layers.py
    # modified to use Leaflet.TileLayer.MBTiles.js
    # make sure this dependency is in your "offline" local folder
    folium.raster_layers.TileLayer._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer.mbTiles(
                {{ this.tiles|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

def main():
    # 是否离线
    offline = True
    # 离线html相关文件的离线包
    offline_file_path = 'offline'
    mbtiles = False
    # titles的文件位置
    tile_path = 'tiles/zhenjiang/{z}/{x}/{y}.png'
    # if using offline resources, override folium .js and .css templates. point to local resources.
    if offline:
        set_offline(offline_file_path)
    else:
        set_online(offline_file_path)
    # if tiles are in .mbtiles format (AS RASTER TILES ONLY), override folium TileLayer template.
    if mbtiles:
        set_mbtiles()

    # ------------------------------------------------
    # 对数据文件预处理
    # 各气象站位置，以及采集数据的文件路径，采用txt格式的文件
    ws_position = {'旧大楼': (119.816647, 32.237348), '扬中变': (119.814105, 32.241109),
                   '开源机房': (119.799526, 32.22298), '新大楼': (119.793075, 32.233924),
                   '新坝变': (119.766776, 32.264969)}
    temp_path = 'measuredata/weatherstation.txt'
    temp_data = rcsv(temp_path)
    # 修正 lon and lat
    names = temp_data['name']
    for i, name in enumerate(names):
        if temp_data.loc[i, 'longitude'] > 125 or temp_data.loc[i, 'longitude'] < 75:
            # 采用内置的坐标
            temp_data.loc[i, 'longitude'], temp_data.loc[i, 'latitude'] = ws_position[name]
    lon, lat = temp_data['longitude'], temp_data['latitude']
    unit = {"temperature": "℃", "pressure": "hPa", "humidity": "%RH", "speed": "m/s", "rainfall": "mm/min",
            "total_radiation": "W/m²", "radiation_all": "MJ/m²", "rainfall_all": "mm", "illumination": "LUX"}

    # vetaLite模板,绘制曲线
    with open('vega/vetalite_temple_one_curve.txt', "r", encoding='utf-8') as f:
        vate_temple_one = json.loads(f.read())
    with open('vega/vetalite_temple_two_curve.txt', "r", encoding='utf-8') as f:
        vate_temple_two = json.loads(f.read())

    # 获得历史数据，直接导入内存因为数据较小，绘制曲线
    hist_data = {}
    for site_name in names:
        hist_path = os.path.join('measuredata', str(site_name) + '.txt')
        hist_data[site_name] = rcsv(hist_path)

    # 绘制温度-------------------------------------------------------------------------------------------
    # 对气象站采集的数据进行异常值处理，正确值的索引为temp_normal_index
    for conduce_data_name in unit.keys():
        # krige插值对象
        krige = nhzn_krige.Krg()
        krige.boundary(shp_path='geodata/shp/镇江市/镇江市.shp')
        # 地图实例对象
        m = folium.Map(
            location=[(krige.lat_max + krige.lat_min) / 2, (krige.lon_max + krige.lon_min) / 2],
            tiles=tile_path,  # str system file path to tile location
            attr='镇江',
            min_zoom=10,  # "zoomed out" value. 0 is the most zoomed out
            max_zoom=13,  # "zoomed in" value. 14 is practical for file size/zoom balance.
            zoom_start=10,
            control_scale=True,  # Whether a zoom control i s added to the map by default.
        )

        # conduce_data_name = "temperature"  # 处理数据的index
        tm = temp_data[conduce_data_name]
        if conduce_data_name in ["rainfall", "rainfall_all", "radiation_all", "total_radiation", "illumination"]:
            vate_temple = vate_temple_one
        else:
            vate_temple = vate_temple_two
        # 针对conduce_data_name 的异常处理，返回正常的index
        temp_normal_index = handing_outliers(tm, conduce_data_name)
        lon_norm, lat_norm, tm_norm = lon[temp_normal_index], lat[temp_normal_index], tm[temp_normal_index]
        tm.astype(float)
        # 获得 geoDataFrame 格式的温度插值数据
        gdf = krige.krg(lon_norm, lat_norm, tm_norm, step=100, conduce_data_name=conduce_data_name)
        # 获得温度的colormap
        colormap = get_colormaps(conduce_data_name, unit)
        colormap.add_to(m)
        # 定义鼠标交互 tooltip
        tooltip = get_tooltip(conduce_data_name)
        # 绘制温度图
        folium.GeoJson(
            gdf,
            style_function=lambda x: {
                "weight": 0,
                "fillColor": colormap(x["properties"][conduce_data_name])
                if x["properties"][conduce_data_name] is not None
                else "transparent",
                "color": "white",
                "fillOpacity": 0.5,
                "line_color": "white",
                "line_opacity": 0,
            },
            tooltip=tooltip
        ).add_to(m)

        # 添加Maker
        m = add_marker(m, vate_temple, lon, lat, tm, names, temp_normal_index, conduce_data_name, unit, hist_data)
        # 保存html 和 图片
        m.save('result/{}.html'.format(conduce_data_name))
        m._to_png(delay=1,  save_name=conduce_data_name)


if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print('运行时间:', end - start)