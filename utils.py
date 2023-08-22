import branca
from folium.features import GeoJsonTooltip


def handing_outliers(data, conduce_data_name):
    if conduce_data_name == 'temperature':
        temp_inrange = data[(data < 40) & (data > -10) & (data != 0)]
        if len(temp_inrange) == 0:
            temp_normal = 0
        else:
            temp_normal = sum(temp_inrange) / len(temp_inrange)
        temp_normal_min = temp_normal - 10
        temp_normal_max = temp_normal + 10
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'pressure':
        temp_inrange = data[(data < 1035) & (data > 990)]
        temp_normal = sum(temp_inrange) / len(temp_inrange)
        temp_normal_min = temp_normal - 20
        temp_normal_max = temp_normal + 20
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'humidity':
        # temp_inrange = data[(data < 100) & (data > 0)]
        # temp_normal = (sum(temp_inrange) - temp_inrange.min() - temp_inrange.max()) / (len(temp_inrange) - 2)
        temp_normal_min = 0
        temp_normal_max = 100
        temp_normal_index = (data <= temp_normal_max) & (data > temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'speed':
        temp_normal_min = 0
        temp_normal_max = 30
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'rainfall':
        temp_normal_min = 0
        temp_normal_max = 5
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'total_radiation':
        temp_normal_min = 0
        temp_normal_max = 1300
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'radiation_all':
        temp_normal_min = 0
        temp_normal_max = 30
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'rainfall_all':
        temp_normal_min = 0
        temp_normal_max = 255
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index
    elif conduce_data_name == 'illumination':
        temp_normal_min = 0
        temp_normal_max = 150000
        temp_normal_index = (data <= temp_normal_max) & (data >= temp_normal_min)
        return temp_normal_index


def get_colormaps(conduce_data_name, unit):
    if conduce_data_name == 'temperature':
        colormap = branca.colormap.LinearColormap(
            vmin=-10,
            vmax=40,
            colors=["#0b6dd4", "#00d458", "#f19f01", "#ff0300"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'pressure':
        colormap = branca.colormap.LinearColormap(
            vmin=996,
            vmax=1030,
            colors=["#01c533", "#e7e703", "#425cff"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'humidity':
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=100,
            colors=["#e9b800", "#04e369", "#03c5f9"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'speed':
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=30,
            colors=["#FFA831", "#c8e225", "#2de66e"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'rainfall':  # 瞬时雨量
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=10,
            colors=["#e09707", "#70dc11", "#0bd0ff"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'total_radiation': # 总辐射
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=1200,
            colors=["#2a81e6", "#55c541", "#f7e53e", "#FF5000"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'radiation_all':  # 累计辐射
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=30,
            colors=["#2a81e6", "#55c541", "#f7e53e", "#FF5000"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'rainfall_all':   # 累计雨量
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=250,
            colors=["#e09707", "#70dc11", "#0bd0ff"],
            caption=unit[conduce_data_name]
        )
        return colormap
    elif conduce_data_name == 'illumination':
        colormap = branca.colormap.LinearColormap(
            vmin=0,
            vmax=15000,
            colors=["#3280ae", "#83e152", "#f8ee50"],
            caption=unit[conduce_data_name]
        )
        return colormap


def get_tooltip(conduce_data_name):
    if conduce_data_name == 'temperature':
        tooltip = GeoJsonTooltip(
            fields=["temperature_str"],
            aliases=["气温:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'pressure':
        tooltip = GeoJsonTooltip(
            fields=["pressure_str"],
            aliases=["大气压力:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'humidity':
        tooltip = GeoJsonTooltip(
            fields=["humidity_str"],
            aliases=["湿度:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'speed':
        tooltip = GeoJsonTooltip(
            fields=["speed_str"],
            aliases=["风速:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'rainfall':
        tooltip = GeoJsonTooltip(
            fields=["rainfall_str"],
            aliases=["雨量:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """
            # max_width=800,
        )
        return tooltip

    elif conduce_data_name == 'total_radiation':
        tooltip = GeoJsonTooltip(
            fields=["total_radiation_str"],
            aliases=["辐射:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                                background-color: #F0EFEF;
                                border: 2px solid black;
                                border-radius: 3px;
                                box-shadow: 3px;
                            """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'radiation_all':
        tooltip = GeoJsonTooltip(
            fields=["radiation_all_str"],
            aliases=["辐射累计:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                                background-color: #F0EFEF;
                                border: 2px solid black;
                                border-radius: 3px;
                                box-shadow: 3px;
                            """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'rainfall_all':
        tooltip = GeoJsonTooltip(
            fields=["rainfall_all_str"],
            aliases=["雨量累计:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                                background-color: #F0EFEF;
                                border: 2px solid black;
                                border-radius: 3px;
                                box-shadow: 3px;
                            """
            # max_width=800,
        )
        return tooltip
    elif conduce_data_name == 'illumination':
        tooltip = GeoJsonTooltip(
            fields=["illumination_str"],
            aliases=["照度:"],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                                background-color: #F0EFEF;
                                border: 2px solid black;
                                border-radius: 3px;
                                box-shadow: 3px;
                            """
            # max_width=800,
        )
        return tooltip


def max_min_anomaly_detection(temp_max, temp_min, conduce_data_name):
    max_norm_index = handing_outliers(temp_max, conduce_data_name)
    min_norm_index = handing_outliers(temp_min, conduce_data_name)
    temp_max_mean = ([t for t, g in zip(temp_max, max_norm_index) if g])
    temp_max_mean = sum(temp_max_mean)/len(temp_max_mean)
    temp_min_mean = ([t for t, g in zip(temp_min, min_norm_index) if g])
    temp_min_mean = sum(temp_min_mean)/len(temp_min_mean)
    for num, g in enumerate(max_norm_index):
        if not g:
            temp_max[num] = temp_max_mean
    for num, g in enumerate(min_norm_index):
        if not g:
            temp_min[num] = temp_min_mean
    # temp_max[[not v for v in max_norm_index]] = sum(temp_max(max_norm_index))/len(temp_max(max_norm_index))
    # temp_min[[not v for v in min_norm_index]] = sum(temp_min(max_norm_index))/len(temp_min(max_norm_index))
    return temp_max, temp_min


def modify_temple(conduce_data_name, unit, temple, site_name, hist_data):
    hist_conduce_data = hist_data[site_name]
    if conduce_data_name == 'temperature':
        # site_name 站储存的数据
        dates, temp_max, temp_min = hist_conduce_data['date'], hist_conduce_data['{}_max'.format(conduce_data_name)].copy(), \
                                    hist_conduce_data['{}_min'.format(conduce_data_name)].copy()
        # 修改数据
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, temp_min = max_min_anomaly_detection(temp_max, temp_min, conduce_data_name)
        for value, date, tmax, tmin in zip(temple['data']['values'], dates, temp_max, temp_min):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['min'] = float(tmin)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
            value['minstr'] = str(tmin) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日最高与最低温度观测值'
        # 修改y title
        temple['layer'][1]['encoding']['y']['axis']['title'] = '温度(℃)'
        # 修改y轴range
        temple['layer'][0]['encoding']['y']['scale']['domain'][0] = min(temp_min) - 5
        temple['layer'][0]['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple

    elif conduce_data_name == 'pressure':
        # site_name 站储存的数据
        dates, temp_max, temp_min = hist_conduce_data['date'], hist_conduce_data['{}_max'.format(conduce_data_name)].copy(), \
                                    hist_conduce_data['{}_min'.format(conduce_data_name)].copy()
        # 修改数据
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, temp_min = max_min_anomaly_detection(temp_max, temp_min, conduce_data_name)
        # 修改数据
        for value, date, tmax, tmin in zip(temple['data']['values'], dates, temp_max, temp_min):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['min'] = float(tmin)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
            value['minstr'] = str(tmin) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日最高与最低大气压力观测值'
        # 修改y title
        temple['layer'][1]['encoding']['y']['axis']['title'] = '大气压力(hPa)'
        # 修改y轴range
        temple['layer'][0]['encoding']['y']['scale']['domain'][0] = min(temp_min) - 5
        temple['layer'][0]['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple
    elif conduce_data_name == 'humidity':
        # site_name 站储存的数据
        dates, temp_max, temp_min = hist_conduce_data['date'], hist_conduce_data['{}_max'.format(conduce_data_name)].copy(), \
                                    hist_conduce_data['{}_min'.format(conduce_data_name)].copy()
        # 修改数据
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, temp_min = max_min_anomaly_detection(temp_max, temp_min, conduce_data_name)
        # 修改数据
        for value, date, tmax, tmin in zip(temple['data']['values'], dates, temp_max, temp_min):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['min'] = float(tmin)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
            value['minstr'] = str(tmin) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日最高与最低大气湿度观测值'
        # 修改y title
        temple['layer'][1]['encoding']['y']['axis']['title'] = '大气湿度(%RH)'
        # 修改y轴range
        temple['layer'][0]['encoding']['y']['scale']['domain'][0] = min(temp_min) - 5
        temple['layer'][0]['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple
    elif conduce_data_name == 'speed':
        # site_name 站储存的数据
        dates, temp_max, temp_min = hist_conduce_data['date'], hist_conduce_data['{}_max'.format(conduce_data_name)].copy(), \
                                    hist_conduce_data['{}_min'.format(conduce_data_name)].copy()
        # 修改数据
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, temp_min = max_min_anomaly_detection(temp_max, temp_min, conduce_data_name)
        # 修改数据
        for value, date, tmax, tmin in zip(temple['data']['values'], dates, temp_max, temp_min):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['min'] = float(tmin)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
            value['minstr'] = str(tmin) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日最高与最低风速观测值'
        # 修改y title
        temple['layer'][1]['encoding']['y']['axis']['title'] = '风速(m/s)'
        # 修改y轴range
        temple['layer'][0]['encoding']['y']['scale']['domain'][0] = min(temp_min) - 5
        temple['layer'][0]['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple

    elif conduce_data_name == 'rainfall':
        dates, temp_max = hist_conduce_data['date'], hist_conduce_data[conduce_data_name].copy()
        # 修改数据
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, _ = max_min_anomaly_detection(temp_max, temp_max, conduce_data_name)
        # 修改数据
        for value, date, tmax in zip(temple['data']['values'], dates, temp_max):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]

        # 修改title
        temple['title']['text'] = site_name + '近15日最高逐分降雨量观测值'
        # 修改y title
        temple['encoding']['y']['axis']['title'] = '雨量(mm/min)'
        # 修改y轴range
        temple['encoding']['y']['scale']['domain'][0] = min(temp_max) - 5
        temple['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple

    elif conduce_data_name == 'total_radiation':
        dates, temp_max = hist_conduce_data['date'], hist_conduce_data[conduce_data_name].copy()
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, _ = max_min_anomaly_detection(temp_max, temp_max, conduce_data_name)
        # 修改数据
        for value, date, tmax in zip(temple['data']['values'], dates, temp_max):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]

        # 修改title
        temple['title']['text'] = site_name + '近15日日最高辐射观测值'
        # 修改y title
        temple['encoding']['y']['axis']['title'] = '总辐射(W/m²)'
        # 修改y轴range
        temple['encoding']['y']['scale']['domain'][0] = min(temp_max) - 5
        temple['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple

    elif conduce_data_name == 'rainfall_all':
        dates, temp_max = hist_conduce_data['date'], hist_conduce_data[conduce_data_name].copy()
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, _ = max_min_anomaly_detection(temp_max, temp_max, conduce_data_name)
        # 修改数据
        for value, date, tmax in zip(temple['data']['values'], dates, temp_max):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]

        # 修改title
        temple['title']['text'] = site_name + '近15日日雨量累计观测值'
        # 修改y title
        temple['encoding']['y']['axis']['title'] = '雨量累计(mm)'
        # 修改y轴range
        temple['encoding']['y']['scale']['domain'][0] = min(temp_max) - 5
        temple['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple
    elif conduce_data_name == 'radiation_all':
        dates, temp_max = hist_conduce_data['date'], hist_conduce_data[conduce_data_name].copy()
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, _ = max_min_anomaly_detection(temp_max, temp_max, conduce_data_name)
        # 修改数据
        for value, date, tmax in zip(temple['data']['values'], dates, temp_max):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日日总辐射量观测值'
        # 修改y title
        temple['encoding']['y']['axis']['title'] = '日辐射量(MJ/m²)'
        # 修改y轴range
        temple['encoding']['y']['scale']['domain'][0] = min(temp_max) - 5
        temple['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple
    elif conduce_data_name == 'illumination':
        dates, temp_max = hist_conduce_data['date'], hist_conduce_data[conduce_data_name].copy()
        # 对temp_max 和 temp_min进行异常值处理
        temp_max, _ = max_min_anomaly_detection(temp_max, temp_max, conduce_data_name)
        # 修改数据
        for value, date, tmax in zip(temple['data']['values'], dates, temp_max):
            value['date'] = str(date)[5:]
            value['max'] = float(tmax)
            value['maxstr'] = str(tmax) + unit[conduce_data_name]
        # 修改title
        temple['title']['text'] = site_name + '近15日日最高照度观测值'
        # 修改y title
        temple['encoding']['y']['axis']['title'] = '照度(LUX)'
        # 修改y轴range
        temple['encoding']['y']['scale']['domain'][0] = min(temp_max) - 5
        temple['encoding']['y']['scale']['domain'][1] = max(temp_max) + 5
        return temple
