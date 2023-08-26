import time
import pandas as pd
import numpy as np
import json
from datetime import datetime
import Coord_Transform as ct

data = {
    "name": "合肥骑行",
    "path": []
}

num_list = [0]
time_list = [None]
ele_list = [None]
lat_list = [None]
lon_list = [None]


def read_gpx(gpx):
    first_str_time = ""
    trkpt_flag = 0
    j = 0

    # num_list = [0]
    # time_list = [None]
    # ele_list = [None]
    # lat_list = [None]
    # lon_list = [None]

    gpx_dict = {}

    for i in range(len(gpx)):
        try:
            ti = str((gpx[i].split("<time>")[1]).split("</time>")[0])
            now_time = time.mktime(time.strptime(ti, "%Y-%m-%dT%H:%M:%S.000Z"))
            first_time = now_time + 28800
            first_str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(first_time))
            break
        except:
            pass
    time_list[0] = first_str_time

    for i in range(len(gpx)):
        if gpx[i].count('<trkpt'):
            trkpt_flag = 1
            j = j + 1
            num_list.append(j)
            time_list.append(j)
            ele_list.append(j)
            lat_list.append(j)
            lon_list.append(j)

        if trkpt_flag == 1:
            try:
                ti = str((gpx[i].split("<time>")[1]).split("</time>")[0])
                now_time = time.mktime(time.strptime(ti, "%Y-%m-%dT%H:%M:%S.000Z"))
                now_str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time + 28800))
                time_list[j] = now_str_time
            except:
                pass

            if gpx[i].count('<trkpt'):
                lat_list[j] = float(gpx[i].split('"')[1])
                lon_list[j] = float(gpx[i].split('"')[3])

            try:
                ele_list[j] = float(str((gpx[i].split("<ele>")[1]).split("</ele>")[0]))
            except:
                pass

        if gpx[i].count('</trkpt>'):
            trkpt_flag = 0

        if gpx[i].count('</trkseg>'):
            break

    gpx_dict["num"] = num_list
    gpx_dict["time"] = time_list
    gpx_dict["lat"] = lat_list
    gpx_dict["lon"] = lon_list
    gpx_dict["ele"] = ele_list

    return gpx_dict


def calculate_speed(time_list, lat_list, lon_list, ele_list):
    if len(time_list) == len(lat_list) and len(time_list) == len(lon_list) and len(time_list) == len(ele_list):
        pass
    else:
        return

    df = pd.DataFrame({'time': time_list, 'lat': lat_list, 'lon': lon_list, 'ele': ele_list})
    columns = df.columns.tolist()

    return df



if __name__ == '__main__':
    path = "./ride-0-2023-08-16-18-22-29.gpx"
    f = open(path, 'r', encoding="utf-8")
    gpx = f.readlines()
    f.close()
    gpx = read_gpx(gpx)
    print(gpx)
    df = calculate_speed(gpx["time"], gpx["lat"], gpx["lon"], gpx["ele"])
    print(df)
    i = 1
    for i in range(1, len(num_list)):
        data['path'].append(ct.wgs84_to_gcj02(lon_list[i], lat_list[i]))
    with open("data.json", "w", encoding="utf-8") as file:
        file.writelines('[')
        json.dump(data, file, ensure_ascii=False)
        file.writelines(']')
