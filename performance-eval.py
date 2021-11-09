
from memory_profiler import profile

@profile
def my_func():
    lifetime_ware_rating = {
        "DELLBOSS VD": 0,
        "MTFDDAV240TCB": 0,
        "MTFDDAV240TDU": 0,
        "SSDSCKKB480G8R": 0,
        "ZA250CM10003": 0,
        "ZA2000CM10002": 0,
        "ZA250CM10002": 0,
        "ZA500CM10002": 0,
        "SSD": 0
    }

    import glob
    import lzma
    import pickle
    import pandas as pd
    import numpy as np
    import os

    #serial_numbers = set()
    failed_drives = {"ssd": [], "hdd": []}

    # year > {"all_drives": set(), "failed_drives": 0}
    year_drives_hdds = {}

    year_drives_ssds = {}

    ssd_models = set()

    for file in sorted(glob.glob("./data/data_*2020.xz")):
        with lzma.open(file, "rb") as f:
            dfs = pickle.load(f)

            for dict_vals in sorted(dfs, key=lambda x: x["filename"]):
                filename = dict_vals["filename"]
                date_df = pd.DataFrame.from_dict(dict_vals["data"])

                date_df["isSSD"] = ~pd.isna(date_df["smart_173_raw"])

                ssds = date_df["smart_173_raw"].count()
                unique_serial_numbers_hdds = date_df["serial_number"][pd.isna(date_df["smart_173_raw"])].unique().tolist()
                unique_serial_numbers_ssds = date_df["serial_number"][~pd.isna(date_df["smart_173_raw"])].unique().tolist()
                ssd_models.update(date_df["model"][~pd.isna(date_df["smart_173_raw"])].unique().tolist())

                year = os.path.basename(filename)[:4]
                if year not in year_drives_hdds.keys():
                    year_drives_ssds[year] = {"all_drives": set(unique_serial_numbers_ssds), "failed_drives": 0}
                    year_drives_hdds[year] = {"all_drives": set(unique_serial_numbers_hdds), "failed_drives": 0}
                else:
                    year_drives_ssds[year]["all_drives"].update(unique_serial_numbers_ssds)
                    year_drives_hdds[year]["all_drives"].update(unique_serial_numbers_hdds)

                failed = date_df.loc[date_df['failure'] == 1]

                year_drives_hdds[year]["failed_drives"] += len(failed[failed["isSSD"] == 0])
                year_drives_ssds[year]["failed_drives"] += len(failed[failed["isSSD"] == 1])

                for index, item in failed.iterrows():
                    if item["model"] in lifetime_ware_rating.keys():
                        failed_drives["ssd"].append(item.to_dict())
                    else:
                        failed_drives["hdd"].append(item.to_dict())
        del f
        del date_df

if __name__ == '__main__':
    my_func()
