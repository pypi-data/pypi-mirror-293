# -*- coding: UTF-8 -*-
"""
@Name:plot_luoqi.py
@Auth:yujw
@Date:2024/8/23-下午3:11
"""
from wz_weather_utils.grid_data import GridData
from wz_weather_utils.calc import calc_wind_dir_and_wind_speed
from wz_weather_plot.plot import DrawImages
from datetime import datetime, timedelta
import pygrib as pg


def plot_ec(time):
    data_path = fr"F:\data\luoqi\EC\{time:%Y%m%d%H}.grib"
    pg_data = pg.open(data_path)

    tem500 = pg_data.select(shortName='t', level=500)[0]
    gh500 = pg_data.select(shortName='z', level=500)[0]
    u850 = pg_data.select(shortName='u', level=850)[0]
    v850 = pg_data.select(shortName='v', level=850)[0]
    latitudes, longitudes = tem500.latlons()
    latitudes = latitudes.reshape(tem500.values.shape)[:, 0]
    longitudes = longitudes.reshape(tem500.values.shape)[0]
    dy, dx = round(latitudes[1] - latitudes[0], 3), round(longitudes[1] - longitudes[0], 3)

    t_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      tem500.values - 273.15)
    z_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      gh500.values / 98)
    u_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      u850.values)
    v_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      v850.values)
    #
    drw = DrawImages(extent=[70, 140, 8, 57])
    drw.set_title(1.02, f"{time + timedelta(hours=8):%Y%m%d%H}BT 500hPa Hgt 850hPa Wind", )
    drw.init_map(line_color="orange")
    drw.sub_nine_map(sub_offset_y=-0.008, line_color="orange")
    wd, ws = calc_wind_dir_and_wind_speed(u_data.values, v_data.values)
    ws_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                       dy, ws)
    drw.contourf(ws_data, levels=[0, 12, 15, 18, 21, 24, 30],
                 colors=["#ffffff", "#B6E8A5", "#7EE55B", "#4ECC43", "#2EB239", "#1E993D"])
    drw.contourf(ws_data, levels=[0, 12, 15, 18, 21, 24, 30],
                 colors=["#ffffff", "#B6E8A5", "#7EE55B", "#4ECC43", "#2EB239", "#1E993D"], sub_ax=drw.sub_ax)
    drw.color_bar(levels=[0, 12, 15, 18, 21, 24, 30],
                  colors=["#ffffff", "#B6E8A5", "#7EE55B", "#4ECC43", "#2EB239", "#1E993D"])
    drw.contour(z_data, levels=range(560, 588, 4), gauss_filter=True, colors="blue", line_widths=1.5, fontcolor="blue",
                fmt="%d")
    drw.contour(z_data, levels=range(560, 588, 4), gauss_filter=True, colors="blue", line_widths=1.5, fontcolor="blue",
                fmt="%d", sub_ax=drw.sub_ax, add_label=False)
    drw.contour(z_data, levels=[588], gauss_filter=True, colors="red", line_widths=2, fontcolor="red", fmt="%d")
    drw.contour(z_data, levels=[588], gauss_filter=True, colors="red", line_widths=2, fontcolor="red", fmt="%d",
                sub_ax=drw.sub_ax, add_label=False)
    drw.contour(z_data, levels=range(592, 600, 4), gauss_filter=True, colors="blue", fontcolor="blue", line_widths=1.5,
                fmt="%d")
    drw.contour(z_data, levels=range(592, 600, 4), gauss_filter=True, colors="blue", fontcolor="blue", line_widths=1.5,
                fmt="%d", sub_ax=drw.sub_ax, add_label=False)
    drw.wind_barbs(u_data, v_data, barb_color="#111111")
    drw.wind_barbs(u_data, v_data, barb_color="#111111", regrid_shape=(6, 6), sub_ax=drw.sub_ax)
    drw.set_review_number()

    drw.save_file(rf"F:\data\luoqi\result\EC\{time:%Y%m%d%H}.png")


def plot_fnl_ec(time):
    # data_path = fr"F:\data\luoqi\fnlec\ec_{time:%Y%m%d%H}.grib"
    data_path = fr"F:\data\luoqi\fnlec\fnl_20210710_12_00.grib2"
    pg_data = pg.open(data_path)

    tem500 = pg_data.select(shortName='t', level=500)[0]
    gh500 = pg_data.select(shortName='gh', level=500)[0]
    u850 = pg_data.select(shortName='u', level=850)[0]
    v850 = pg_data.select(shortName='v', level=850)[0]
    latitudes, longitudes = tem500.latlons()
    latitudes = latitudes.reshape(tem500.values.shape)[:, 0]
    longitudes = longitudes.reshape(tem500.values.shape)[0]
    dy, dx = round(latitudes[1] - latitudes[0], 3), round(longitudes[1] - longitudes[0], 3)

    t_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      tem500.values - 273.15)
    # z_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
    #                   dy,
    #                   gh500.values / 98)
    # z_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
    #                   dy,
    #                   gh500.values * 0.1)
    u_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      u850.values)
    v_data = GridData(latitudes[0], latitudes[-1], longitudes[0], longitudes[-1], len(longitudes), len(latitudes), dx,
                      dy,
                      v850.values)
    #
    drw = DrawImages(extent=[30, 170, -10, 70],dpi=600)
    drw.set_title(1.02, f"{time + timedelta(hours=8):%Y%m%d%H}BT 500hPa Hgt-Tem  850hPa Wind", )
    drw.init_map(line_color="orange", add_province=False, add_city=False, add_chn_border=False)
    # drw.sub_nine_map(sub_offset_y=-0.008, line_color="orange")

    # drw.contour(t_data, levels=range(-30, 3, 2), gauss_filter=True, colors="red", line_widths=1.5, fontcolor="red",
    #             sigma=3,
    #             fmt="%d")
    # drw.contour(t_data, levels=range(-30, 3, 2), gauss_filter=True, colors="red", line_widths=1.5, fontcolor="red",
    #             sigma=4,
    #             fmt="%d", sub_ax=drw.sub_ax, add_label=False)
    # drw.contour(z_data, levels=range(560, 588, 4), gauss_filter=True, colors="blue", line_widths=1.5 / 3,
    #             fontcolor="blue", fontsize=5,
    #             sigma=4,  fmt="%d")
    # # drw.contour(z_data, levels=range(560, 588, 4), gauss_filter=True, colors="blue", line_widths=1.5, fontcolor="blue",fontsize=10,
    # #             sigma=4,
    # #             fmt="%d", sub_ax=drw.sub_ax, add_label=False)
    # drw.contour(z_data, levels=[588], gauss_filter=True, colors="blue", line_widths=2 / 3, fontcolor="blue", fontsize=5,
    #             fmt="%d", sigma=4)
    # # drw.contour(z_data, levels=[588], gauss_filter=True, colors="blue", line_widths=2, fontcolor="blue", fmt="%d",
    # #             sigma=4,
    # #             sub_ax=drw.sub_ax, add_label=False)
    # drw.contour(z_data, levels=range(592, 600, 4), gauss_filter=True, colors="blue", fontcolor="blue",
    #             line_widths=1.5 / 3, fontsize=5,
    #             sigma=4, fmt="%d")
    # drw.contour(z_data, levels=range(592, 600, 4), gauss_filter=True, colors="blue", fontcolor="blue", line_widths=1.5,
    #             sigma=4, fmt="%d", sub_ax=drw.sub_ax, add_label=False)
    drw.wind_barbs(u_data, v_data, barb_color="#27408b", length=3.5, line_width=0.3, regrid_shape=34)
    # drw.wind_barbs(u_data, v_data, barb_color="#111111", regrid_shape=(6, 6), sub_ax=drw.sub_ax)
    # drw.set_review_number()

    drw.save_file(rf"F:\data\luoqi\result\ec_fnl\fnl_{time:%Y%m%d%H}.png")


def plot_tmp(time):
    # data_path = fr"F:\data\luoqi\fnlec\ec_{time:%Y%m%d%H}.grib"
    drw = DrawImages(extent=[50, 160, -10, 70])
    drw.init_map(line_color="orange", add_province=False, add_city=False)

    drw.save_file(rf"./test2.eps")


# for t in [datetime(2021, 7, 11, 0), datetime(2021, 7, 11, 6),
#           datetime(2021, 7, 11, 12), datetime(2021, 7, 11, 18)]:
#     process(t)
plot_fnl_ec(datetime(2021, 7, 10, 12))
# plot_tmp(datetime(2021, 7, 10, 12))
