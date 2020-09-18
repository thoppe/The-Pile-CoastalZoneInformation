import json
import time
from dspipe import Pipe

import pandas as pd
from utils import get_package_page


"""
Download package information for each item in the collection
Uses: https://api.govinfo.gov/docs/
"""

sleep_time = 1

# First, get a collection of the packages
def collect(f0):

    with open(f0) as FIN:
        js = json.load(FIN)

    df = pd.DataFrame(js["packages"])
    return df


df = pd.concat(Pipe(f"data/collection_info/", shuffle=True, limit=None)(collect, -1))


def compute(f0, f1):

    js = get_package_page(f0)
    js = json.dumps(js, indent=2)

    print(js)

    with open(f1, "w") as FOUT:
        FOUT.write(js)

    time.sleep(sleep_time)


P = Pipe(
    df.packageId,
    f"data/package_info",
    output_suffix=".json",
    autoname=False,
    shuffle=True,
)
P(compute, 5)
