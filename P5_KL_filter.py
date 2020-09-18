import jsonlines
import numpy as np
from dspipe import Pipe
import collections
import re
import pandas as pd

f_jsonl_input = "data/GOVINFO_CZIC_unfiltered.jsonl"
f_jsonl_output = "data/GOVINFO_CZIC_KL.jsonl"

KL_cutoff = 2.0
n_debug_limit = None

"""
Use the Kullback–Leibler divergence on character bigrams to filter lines.
"""


def compute_bigrams(text):
    cx = collections.Counter()
    pairs = [x0 + x1 for x0, x1 in zip(text, text[1:])]
    cx.update(pairs)
    return cx


def compute(js):
    line_cx = collections.Counter()
    text = js["text"]

    for line in text.split("\n"):
        if not line:
            continue

        line_cx.update(compute_bigrams(line))

    return line_cx


ngrams = collections.Counter()

with jsonlines.open(f_jsonl_input) as FIN:
    for block in Pipe(FIN, limit=n_debug_limit)(compute, -1):
        ngrams.update(block)

df = pd.DataFrame(index=ngrams.keys())
df["observations"] = ngrams.values()
Q = df.observations / df.observations.sum()


def compute2(js):
    text = js["text"]
    output = []

    for line in text.split("\n"):
        if not line:
            output.append(line)
            continue

        line_cx = compute_bigrams(line)
        df = pd.DataFrame(index=line_cx.keys())
        df["observations"] = line_cx.values()
        P = df.observations / df.observations.sum()
        P = P.reindex(Q.index).fillna(0)

        idx = P > 0
        KL = (P[idx] * np.log(P[idx] / Q[idx])).sum()

        if KL > KL_cutoff:
            continue

        output.append(line)

    text2 = "\n".join(output)
    text2 = re.sub("[\n]+", "\n", text2)

    js["text"] = text2
    js["meta"]["KL_bigram_filter_cutoff"] = KL_cutoff
    js["meta"]["KL_bigram_filter_frac_removed"] = 1 - float(len(text2)) / len(text)
    print(js["meta"]["KL_bigram_filter_frac_removed"])
    return js["text"]


with jsonlines.open(f_jsonl_input) as FIN, jsonlines.open(f_jsonl_output, "w") as FOUT:
    for js in Pipe(FIN, limit=n_debug_limit)(compute2, -1):
        FOUT.write(js)
