import numpy as np
from bs4 import BeautifulSoup
import requests
import zipfile
import os
from urllib.parse import urlparse
import glob
import io
import zipfile
import pandas as pd
import lzma
import pickle

from requests_html import HTMLSession

session = HTMLSession()

response = session.get("https://www.backblaze.com/b2/hard-drive-test-data.html")
response.html.render()

soup = BeautifulSoup(response.html.html, "html.parser")

data_blocks = soup.find_all("div", class_="data", recursive=True)

download_locations = []
for data in data_blocks:
    link = data.find("a", class_="download-data-files")["href"]
    download_locations.append(link)

print(download_locations)


def download_extract_zip(url):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            with thezip.open(zipinfo) as thefile:
                yield zipinfo.filename, thefile

def download_file(url, save_path):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(save_path, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return os.path.join(save_path, local_filename)


for file in download_locations:
    filename = os.path.basename(urlparse(file).path)
    if not os.path.isfile("data/" + filename):
        print(f"Downloading: {file}")
        download_file(file, "./data")


atters_to_keep = ["date","serial_number","model","capacity_bytes","failure",
                  "smart_9_normalized","smart_9_raw",
                  "smart_173_normalized","smart_173_raw",
                  "smart_231_normalized","smart_231_raw",
                  "smart_241_normalized","smart_241_raw",
                  "smart_242_normalized","smart_242_raw"]
for file in glob.glob("./data/*.zip"):
    if not os.path.isfile(file[:-4]+".xz"):
        dfs = []
        with zipfile.ZipFile(file, 'r') as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    if ".csv" in zipinfo.filename and "__MACOSX" not in zipinfo.filename:
                        print(zipinfo.filename)
                        df = pd.read_csv(thefile)
                        if not df.empty:
                            try:
                                df = df[atters_to_keep]
                            except KeyError as e:
                                if "smart_173" in str(e):
                                    df["smart_173_normalized"] = df.shape[0] * [np.NaN]
                                    df["smart_173_raw"] = df.shape[0] * [np.NaN]

                                if "smart_231" in str(e):
                                    df["smart_231_normalized"] = df.shape[0] * [np.NaN]
                                    df["smart_231_raw"] = df.shape[0] * [np.NaN]

                                df = df[atters_to_keep]

                            dfs.append({"data": df.to_dict(), "filename": file[:-4]+"/"+os.path.basename(zipinfo.filename)})

        with lzma.open(f"{file[:-4]}.xz", "wb") as f:
            pickle.dump(dfs, f)
