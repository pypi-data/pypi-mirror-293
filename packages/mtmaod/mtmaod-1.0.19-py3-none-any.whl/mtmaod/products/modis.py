import os

import numpy as np
import numpy.ma as ma
import pandas as pd

from mtmaod.path import Extractor
from mtmaod.utils.netCDF4 import NetCDF4
from mtmaod.utils.pyhdf import SDS, PyHDF

from ._template import (
    SatelliteProductDataNetCDF4,
    SatelliteProductDataPyHDF,
    SatelliteProductReaderNetCDF4,
    SatelliteProductReaderPyHDF,
)


# ===================================================================================================
class MXD02Data(SatelliteProductDataPyHDF):

    def scale_and_offset(self, data: np.ndarray):
        infos: dict = self.infos()
        radiance_scales = MXD02Data.value_set_decimal(infos.get("reflectance_scales", 1), decimal=None)
        radiance_offsets = MXD02Data.value_set_decimal(infos.get("reflectance_offsets", 0), decimal=None)
        fill_value = infos.get("_FillValue")
        _data = ma.masked_values(data, fill_value, rtol=1e-8, atol=1e-9)
        return radiance_scales * (_data - radiance_offsets)


class MXD02Reader(SatelliteProductReaderPyHDF):
    Product_File_Time_Format = "[.]A%Y%j[.]%H%M[.]"
    LinkedDataClass = MXD02Data

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = PyHDF.read(fp, dataset_name, *args, **kwargs)
        DataClass = MXD02Reader.LinkedDataClass
        return DataClass(dp, isRaw=isRaw)

    @staticmethod
    def table_scales_and_offsets(fp, *args, **kwargs):
        bands = ["EV_1KM_RefSB", "EV_1KM_Emissive", "EV_250_Aggr1km_RefSB", "EV_500_Aggr1km_RefSB"]
        columns = [
            "band_names",
            "reflectance_scales",
            "reflectance_offsets",
            "radiance_scales",
            "radiance_offsets",
            "corrected_counts_scales",
            "corrected_counts_offsets",
        ]
        indexes_string = "1,2,3,4,5,6,7,8,9,10,11,12,13lo,13hi,14lo,14hi,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"
        indexes = indexes_string.split(",")
        df_list = []
        for band in bands:
            info = MXD02Reader.read(fp, band, *args, **kwargs).infos()
            info["band_names"] = info.get("band_names").split(",")
            _info = {k: info[k] for k in columns if k in info}
            df_list.append(pd.DataFrame(_info))
        return pd.concat(df_list, ignore_index=True).set_index("band_names").loc[indexes, :]


# ===================================================================================================
class MXD04L2Reader(SatelliteProductReaderPyHDF):
    Product_File_Time_Format = "[.]A%Y%j[.]%H%M[.]"
    LinkedDataClass = SatelliteProductDataPyHDF
    Band_Latitude = "Latitude"
    Band_Longitude = "Longitude"

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = PyHDF.read(fp, dataset_name, *args, **kwargs)
        DataClass = MXD04L2Reader.LinkedDataClass
        return DataClass(dp, isRaw=isRaw)


# ===================================================================================================
class MXD09Reader(SatelliteProductReaderPyHDF):
    Product_File_Time_Format = "[.]A%Y%j[.]"
    LinkedDataClass = SatelliteProductDataPyHDF

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = PyHDF.read(fp, dataset_name, *args, **kwargs)
        DataClass = MXD09Reader.LinkedDataClass
        return DataClass(dp, isRaw=isRaw)


# ===================================================================================================
class MXDLabGridReader(SatelliteProductReaderNetCDF4):
    Product_File_Time_Format = "[.]%Y%j%H%M%S[.]"  # MOD021KM_L.1000.2021001040500.H26V05.000000.h5
    LinkedDataClass = SatelliteProductDataNetCDF4

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = NetCDF4.read(fp, dataset_name, *args, **kwargs)
        DataClass = MXDLabGridReader.LinkedDataClass
        return DataClass(dp, isRaw=isRaw)


# ===================================================================================================
class MCD19A2Reader(SatelliteProductReaderPyHDF):
    Product_File_Time_Format = "MCD19A2[.]A%Y%j[.]"
    LinkedDataClass = SatelliteProductDataPyHDF

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = PyHDF.read(fp, dataset_name, *args, **kwargs)
        DataClass = MCD19A2Reader.LinkedDataClass
        return DataClass(dp, isRaw=isRaw)

    @staticmethod
    def list_orbit_times(fp):
        return [i for i in fp.attributes()["Orbit_time_stamp"].split(" ") if i]

    # @staticmethod
    # def open_adjacent_files(data_file, data_files: list, *args, **kwargs):
    #     # MCD19A2.A2020001.h04v09.061.2023132152021.hdf
    #     func_ext_hv = Extractor.file_hv()
    #     hv = func_ext_hv(data_file)
    #     h, v = int(hv[1:3]), int(hv[4:6])
    #     h_min, h_max = str(h - 1).zfill(2) if (h - 1) >= 0 else "35", str(h + 1).zfill(2) if (h + 1) <= 35 else "00"
    #     v_min, v_max = str(v - 1).zfill(2), str(v + 1).zfill(2)
    #     adjacent_files = {
    #         "nw": f"h{h_min}v{v_min}",
    #         "n": f"h{h}v{v_min}",
    #         "ne": f"h{h_max}v{v_min}",
    #         "w": f"h{h_min}v{v}",
    #         "c": f"h{h}v{v}",
    #         "e": f"h{h_max}v{v}",
    #         "sw": f"h{h_min}v{v_max}",
    #         "s": f"h{h}v{v_max}",
    #         "se": f"h{h_max}v{v_max}",
    #     }
    #     str_date = os.path.basename(data_file).split(".")[1]
    #     adjacent_file_points = {}
    #     for k, v in adjacent_files.items():
    #         for _file in data_files:
    #             _file_name = os.path.basename(_file)
    #             if v in _file_name and str_date in _file_name:
    #                 adjacent_file_points[k] = PyHDF.open(_file, *args, **kwargs)
    #                 break
    #     return adjacent_file_points

    # @staticmethod
    # def merge_adjascent_files(fps: dict, dataset_name, *args, isRaw=False, **kwargs):
    #     times = MCD19A2Reader.list_orbit_times(fps["c"])
    #     central_data = MCD19A2Reader.read(fps["c"], dataset_name, *args, isRaw=isRaw, **kwargs)[:]
    #     band, height, width = central_data.shape[-2:]
    #     arr = np.zeros((band, height * 3, width * 3), dtype=central_data.dtype)
    #     mask = np.zeros((band, height * 3, width * 3), dtype=bool)
    #     arr[:, height : 2 * height, width : 2 * width] = central_data
    #     mask[:, height : 2 * height, width : 2 * width] = True
    #     for _time in times:
    #         for k, v in fps.items():
    #             if k == "c":
    #                 continue
    #             dp = PyHDF.read(v, dataset_name, *args, **kwargs)
    #             dp_c = PyHDF.read(fps["c"], dataset_name, *args, **kwargs)
    #             dp.data = np.concatenate((dp_c.data, dp.data), axis=0)
    #             dp_c.data = None
    #     return data
