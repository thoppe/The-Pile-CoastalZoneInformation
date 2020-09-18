import dspipe
from wasabi import msg
import time, json
import pandas as pd
from pathlib import Path
from utils import get_collection_page

"""
Download the package IDs from https://api.govinfo.gov/docs/
"""

# df = pd.read_csv("data/collection_names.csv")
save_dest = Path("data/collection_info")
save_dest.mkdir(exist_ok=True, parents=True)
# print(df)

collection_name = "CZIC"
n_rows = 4888


def download_collection(row):

    collectionCode, packageCount = row

    ITR = [(collectionCode, n) for n in range(0, packageCount, 100)]

    msg.info(f"{collectionCode} {packageCount}")

    for offset in range(0, packageCount, 100):

        f_save = save_dest / f"{collectionCode}_{offset:08d}.json"

        if f_save.exists():
            continue

        try:
            js = get_collection_page(collectionCode, offset)
        except:
            print(f"ERROR ON {row} {offset}")
            break

        js = json.dumps(js, indent=2)
        msg.good(f"Saved {f_save}")

        with open(f_save, "w") as FOUT:
            FOUT.write(js)

        time.sleep(0)


download_collection((collection_name, n_rows))

# ITR = [(name, count) for name, count in zip(df.collectionCode, df.packageCount)]

# dspipe.Pipe(ITR, save_dest, autoname=False,
#            shuffle=False)(download_collection, 1)
