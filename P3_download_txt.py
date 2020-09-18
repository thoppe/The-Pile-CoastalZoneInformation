import json
import time
from dspipe import Pipe

import pandas as pd
from utils import govinfo_download

import bs4

n_downloads = 8


"""
Download html information for each item in the collection
Uses: https://api.govinfo.gov/docs/
"""

sleep_time = 1


def compute(f0, f1):

    with open(f0) as FIN:
        js = json.load(FIN)

    try:
        url = js["download"]["txtLink"]
    except KeyError:
        print(f"No text link for {f0}")
        exit()

    if url[-4:] != "/htm":
        print("Expected HTM LINK", url)
        exit()

    raw = govinfo_download(url, as_json=False)
    text = bs4.BeautifulSoup(raw, "lxml").text

    with open(f1, "w") as FOUT:
        FOUT.write(text)

    print(f0, len(text))

    time.sleep(sleep_time)


P = Pipe(
    f"data/package_info",
    "data/htm_text",
    output_suffix=".txt",
    input_suffix=".json",
    shuffle=True,
)
P(compute, n_downloads)
