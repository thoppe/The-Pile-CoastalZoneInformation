import json
import jsonlines
from pathlib import Path
from dspipe import Pipe
from pdf_filter import pdf_filter

collectionName = "CZIC"


def compute(f0):

    with open(f0) as FIN:
        raw = FIN.read()
        text = "\n".join([line.strip() for line in raw.split("\n")])
        text = pdf_filter(text)

    f_meta = str(Path("data/package_info/") / f0.name[:-4]) + ".json"

    with open(f_meta) as FIN:
        meta = json.load(FIN)

    return {
        "meta": meta,
        "text": text,
    }


P = Pipe("data/htm_text", output_suffix=".txt", shuffle=True)

with jsonlines.open(f"data/GOVINFO_{collectionName}_unfiltered.jsonl", "w") as FOUT:
    for row in P(compute, -1):
        FOUT.write(row)
